import django

from pgmigrate.action import (
    BlockingAction,
    Show,
    Terminate,
)
from pgmigrate.version import __version__

__all__ = ["BlockingAction", "Show", "Terminate", "__version__"]

if django.VERSION < (3, 2):  # pragma: no cover
    default_app_config = "pgmigrate.apps.PGMigrateConfig"

del django
