import django.apps

from pgmigrate import core  # noqa


class PGMigrateConfig(django.apps.AppConfig):
    name = "pgmigrate"

    def ready(self):
        core.patch_load_command_class()
