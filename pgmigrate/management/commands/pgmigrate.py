import functools
import inspect
import sys

import pgactivity
import pglock
from django.core.exceptions import ImproperlyConfigured
from django.core.management.commands.migrate import Command as MigrateCommand
from django.db import connections
from django.db.utils import OperationalError

try:
    import psycopg.errors as psycopg_errors
except ImportError:
    import psycopg2.errors as psycopg_errors
except Exception as exc:  # pragma: no cover
    raise ImproperlyConfigured("Error loading psycopg2 or psycopg module") from exc

from pgmigrate import action, config


class Command(MigrateCommand):
    def handle(self, *args, **options):
        if (
            options["database"] not in connections
            or connections[options["database"]].vendor != "postgresql"
        ):  # pragma: no cover
            return super().handle(*args, **options)

        if options["verbosity"]:
            self.stdout.write(
                self.style.MIGRATE_HEADING("Postgres process ID: ") + str(pgactivity.pid())
            )

        blocking_action = config.blocking_action()
        blocking_action = (
            blocking_action() if inspect.isclass(blocking_action) else blocking_action
        )

        if blocking_action and not isinstance(
            blocking_action, action.BlockingAction
        ):  # pragma: no cover
            raise TypeError("Blocking actions must inherit pgmigrate.BlockingAction.")

        try:
            prioritize_kwargs = {
                "interval": config.blocking_action_interval(),
                "side_effect": functools.partial(blocking_action, self)
                if blocking_action
                else None,
            }
            if config.lock_timeout():
                prioritize_kwargs["timeout"] = config.lock_timeout()

            with pglock.prioritize(**prioritize_kwargs):
                return super().handle(*args, **options)
        except OperationalError as exc:
            if exc.__cause__.__class__ == psycopg_errors.LockNotAvailable:
                if self.verbosity:  # pragma: no branch
                    self.stdout.write(self.style.ERROR("\nLock timeout expired. Aborting..."))

                sys.exit(1)
            else:  # pragma: no cover
                raise
