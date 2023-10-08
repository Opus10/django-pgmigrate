import datetime as dt
import threading
import time

import pglock
import pytest
from django.core.management import call_command
from django.db import transaction
from django.db.utils import OperationalError

import pgmigrate


@pytest.mark.django_db
def test_migrate_terminate(reraise, capsys):
    barrier = threading.Barrier(2)

    @reraise.wrap
    def migrate():
        barrier.wait(timeout=5)
        call_command("migrate", "auth", "0008")
        captured = capsys.readouterr()
        assert "Terminated" in captured.out

        barrier.wait(timeout=5)
        call_command("migrate", "-v", 0)
        captured = capsys.readouterr()
        assert captured.out == ""

    @reraise.wrap
    def block():
        with pytest.raises(OperationalError, match="terminat"):
            with transaction.atomic():
                pglock.model("auth.User", timeout=0)
                barrier.wait(timeout=5)
                time.sleep(5)

        with pytest.raises(OperationalError, match="terminat"):
            with transaction.atomic():
                pglock.model("auth.User", timeout=0)
                barrier.wait(timeout=5)
                time.sleep(5)

    migrate_thread = threading.Thread(target=migrate)
    block_thread = threading.Thread(target=block)
    migrate_thread.start()
    block_thread.start()
    migrate_thread.join()
    block_thread.join()


@pytest.mark.django_db
def test_migrate_show(reraise, capsys, settings):
    settings.PGMIGRATE_BLOCKING_ACTION = pgmigrate.Show
    barrier = threading.Barrier(3)

    @reraise.wrap
    def migrate():
        barrier.wait(timeout=5)
        call_command("migrate", "auth", "0008")
        captured = capsys.readouterr()
        assert "Blocked by" in captured.out

        barrier.wait(timeout=5)
        call_command("migrate", "-v", 0)
        captured = capsys.readouterr()
        assert "Blocked by" not in captured.out

    @reraise.wrap
    def terminate():
        barrier.wait(timeout=5)
        time.sleep(3.0)
        call_command("pglock", "--blocking", "--terminate", "--yes")

        barrier.wait(timeout=5)
        time.sleep(1.5)
        call_command("pglock", "--blocking", "--terminate", "--yes")

    @reraise.wrap
    def block():
        with pytest.raises(OperationalError, match="terminat"):
            with transaction.atomic():
                pglock.model("auth.User", timeout=0)
                barrier.wait(timeout=5)
                time.sleep(5)

        with pytest.raises(OperationalError, match="terminat"):
            with transaction.atomic():
                pglock.model("auth.User", timeout=0)
                barrier.wait(timeout=5)
                time.sleep(5)

    migrate_thread = threading.Thread(target=migrate)
    block_thread = threading.Thread(target=block)
    terminate_thread = threading.Thread(target=terminate)
    migrate_thread.start()
    block_thread.start()
    terminate_thread.start()
    migrate_thread.join()
    block_thread.join()
    terminate_thread.join()


@pytest.mark.django_db
def test_migrate_timeout(reraise, capsys, settings):
    settings.PGMIGRATE_BLOCKING_ACTION = None
    settings.PGMIGRATE_LOCK_TIMEOUT = dt.timedelta(milliseconds=100)
    barrier = threading.Barrier(2)

    @reraise.wrap
    def migrate():
        barrier.wait(timeout=5)
        with pytest.raises(SystemExit):
            call_command("migrate", "auth", "0008")
        captured = capsys.readouterr()
        assert "timeout expired" in captured.out

        barrier.wait(timeout=5)

    @reraise.wrap
    def block():
        with transaction.atomic():
            pglock.model("auth.User", timeout=0)
            barrier.wait(timeout=5)
            barrier.wait(timeout=5)

    migrate_thread = threading.Thread(target=migrate)
    block_thread = threading.Thread(target=block)
    migrate_thread.start()
    block_thread.start()
    migrate_thread.join()
    block_thread.join()
