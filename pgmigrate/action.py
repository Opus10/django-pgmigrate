import pglock


class BlockingAction(pglock.PrioritizeSideEffect):
    """
    The base class for writing custom actions for managing blocking
    migration activitiy.

    Implement the `worker` method, which is supplied:

    1. The migrate management command instance.
    2. The `pglock.models.BlockedPGLock` queryset
       of all blocked migration operations.
    """

    def worker(self, cmd, blocked_locks):
        raise NotImplementedError

    def __call__(self, cmd, blocked_locks):
        return self.worker(cmd, blocked_locks.filter(**self.filters))


class Terminate(BlockingAction):
    """Terminate all blocking locks when running migrations"""

    def worker(self, cmd, blocking_locks):
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


class Show(BlockingAction):
    """
    Show all blocking locks when running migrations.
    The process IDs are shown, which can be used in calls to the `pgactivity`
    management command.
    """

    def worker(self, cmd, blocking_locks):
        if not hasattr(cmd, "_pgmigrate_last_output"):
            cmd._pgmigrate_last_output = ""

        blocking_pids = list(
            blocking_locks.values_list("blocking_activity_id", flat=True).distinct()
        )
        if blocking_pids:
            pluralize = "ies" if len(blocking_locks) != 1 else "y"
            pids_str = " ".join(str(pid) for pid in blocking_pids)
            output = cmd.style.WARNING(
                f"\n  Blocked by {len(blocking_pids)} quer{pluralize}: {pids_str}..."
            )

            if output != cmd._pgmigrate_last_output and cmd.verbosity:
                cmd.stdout.write(output, ending=" ")

            cmd._pgmigrate_last_output = output

        return blocking_pids
