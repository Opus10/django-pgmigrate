.. _advanced:

Advanced Configuration
======================

Here cover more advanced configuration scenarios.

Customizing the Blocking Action
-------------------------------

By default, ``settings.PGMIGRATE_BLOCKING_ACTION`` is set to ``pgmigrate.Terminate``,
meaning blocking queries are automatically terminated. It can also be
set to ``pgmigrate.Show`` to show blocking queries or ``None`` to disable any
action altogether.

You can supply a custom action to ``settings.PGMIGRATE_BLOCKING_ACTION`` to
further customize what happens when migrations are blocked. Inherit ``pgmigrate.BlockingAction``
and implement the ``worker`` method, which takes the migrate management command
instance and a ``pglock.models.BlockedPGLock`` queryset matching
all blocking locks. The function returns the blocking locks that
were handled.

Here's what the ``pgmigrate.Terminate`` action looks like:

.. code-block:: python

    import pgmigrate

    class Terminate(pgmigrate.BlockingAction):
        def worker(self, cmd, blocking_locks):
            """
            A periodic background task that terminates blocking locks.

            Args:
                cmd: The instance of the "migrate" management command
                blocking_locks: A queryset of matching locks using the
                    ``BlockedPGLock`` model from the ``django-pglock`` library.
            """
            terminated = blocking_locks.terminate_blocking_activity()

            if terminated:  # pragma: no branch
                pluralize = "ies" if len(terminated) != 1 else "y"
                if cmd.verbosity:
                    cmd.stdout.write(
                        cmd.style.WARNING(
                            f"\n  Terminated {len(terminated)} blocking quer{pluralize}..."
                        ),
                        ending=" ",
                    )

            return terminated

Remember, the action is ran periodically during migrations. Above we're using ``cmd.stdout``
to print messages because ``cmd`` is an instance of a management command. See
`the Django docs <https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/>`__
for more information on how management commands work.

Consult the `django-pglock docs <https://django-pglock.readthedocs.io>`__ for more information
on how to use the ``BlockedPGLock`` model and queryset methods.

Configuring the Blocking Action Interval
----------------------------------------

By default, blocking actions are ran every second. Supply a ``datetime.timedelta`` object
to ``settings.PGMIGRATE_BLOCKING_ACTION_INTERVAL`` to change this.

Disabling Patching of the Migrate Command
-----------------------------------------

By default, the ``migrate`` command is patched to use the ``pgmigrate`` command from ``django-pgmigrate``.
If this isn't desirable, set ``settings.PGMIGRATE_PATCH_MIGRATE`` to ``False``.

If disabled, you'll need to run the ``pgmigrate`` management command to apply migrations
and use the features of ``django-pgmigrate``.