import datetime as dt

from django.conf import settings

from pgmigrate import action


def lock_timeout():
    """Configure the lock timeout for the migrate command"""
    return getattr(settings, "PGMIGRATE_LOCK_TIMEOUT", None)


def blocking_action():
    """
    Configure the action that should be taken when blocking locks
    are discovered during migrations. Must be:

    * `pgmigrate.Terminate`: To terminate the blocking locks
    * `pgmigrate.Show`: To show the process IDs of the blocking locks
    * A custom action that inherits `pgmigrate.BlockingAction`
      and implements the `worker` method.
    """
    return getattr(settings, "PGMIGRATE_BLOCKING_ACTION", action.Terminate)


def blocking_action_interval():
    """
    Configure the interval at which blocking actions run.
    """
    return getattr(settings, "PGMIGRATE_BLOCKING_ACTION_INTERVAL", dt.timedelta(seconds=1))


def patch_migrate():
    """True if the migrate command should be patched with the pgmigrate command"""
    return getattr(settings, "PGMIGRATE_PATCH_MIGRATE", True)
