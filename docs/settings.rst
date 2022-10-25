.. _settings:

Settings
========

Below are all settings for ``django-pgmigrate``.

PGMIGRATE_BLOCKING_ACTION
-------------------------

Configure the action that should be taken when blocking locks
are discovered during migrations. Must be:

* ``pgmigrate.TERMINATE``: To terminate the blocking locks
* ``pgmigrate.SHOW``: To show the process IDs of the blocking locks
* ``None``: To take no action
* A custom function that takes the managment command instance and
  the blocking lock queryset. See the :ref:`advanced` section for an example.

**Default** ``pgmigrate.TERMINATE``

PGMIGRATE_BLOCKING_ACTION_INTERVAL
----------------------------------

Configure the interval at which the blocking action runs using a ``datetime.timedelta`` object.

**Default** ``datetime.timedelta(seconds=1)``

PGMIGRATE_LOCK_TIMEOUT
----------------------

Use a Python ``datetime.timedelta`` object to configure Postgres's ``lock_timeout`` for migrations.

**Default** ``None``

PGMIGRATE_PATCH_MIGRATE
-----------------------

``True`` if Django's ``migrate`` command is patched to use the ``pgmigrate`` command.
If ``False``, one must call ``python manage.py pgmigrate`` to use
special migration functionality.

**Default** ``True``