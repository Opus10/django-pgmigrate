from django.core import management

from pgmigrate import config
from pgmigrate.management.commands.pgmigrate import Command

_real_load_command_class = management.load_command_class


def load_command_class(app_name, name):
    if app_name == "django.core" and name == "migrate":
        return Command()
    else:
        return _real_load_command_class(app_name, name)


def patch_load_command_class():
    """
    Patches Django's load_command_class to use the "pgmigrate" command
    instead of "migrate".
    """
    if config.patch_migrate():  # pragma: no branch
        management.load_command_class = load_command_class
