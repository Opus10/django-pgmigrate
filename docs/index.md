# django-pgmigrate

`django-pgmigrate` helps you avoid costly downtime with Postgres migrations.

Imagine the following happens:

1. A long-running task queries a model in a transaction and keeps the transaction open.
2. `python manage.py migrate` tries to change a field on the model.

Because of how Postgres queues locks, this common scenario causes **every** subsequent query on the model to block until the query from 1) has finished.

`django-pgmigrate` provides the following features to alleviate problematic locking scenarios when running migrations:

* Detect blocking queries and terminate them automatically (the default behavior).
* Print blocking queries so that you can inspect and terminate them manually.
* Set the lock timeout so that migrations are terminated if they block too long.

## Quick Start

After following the [installation](installation.md) section, running `python manage.py migrate` will automatically terminate any blocking queries. Here's an example of what it looks like:

![Terminate Blocking](static/terminate_blocking.png)

There are two additional outputs in the `migrate` command versus the original:

1. The first output line shows the Postgres process ID. This is useful for querying activity that's blocking the process.
2. The yellow text shows when a blocking query was detected and terminated. In our case, it was blocking auth migration 12.

You can configure `django-pgmigrate` to show blocked queries instead of automatically killing them, and you can also set the lock timeout to automatically cancel migrations if they block for too long. See the next steps below for more details.

## Compatibility

`django-pgmigrate` is compatible with Python 3.8 - 3.12, Django 3.2 - 4.2, Psycopg 2 - 3, and Postgres 12 - 16.

## Next Steps

We recommend everyone first read:

* [Installation](installation.md) for how to install the library.

After this, there are several usage guides:

* [Automatically Terminating Blocking Queries](automatic.md) for more information on how blocking queries are automatically terminated.
* [Manually Terminating Blocking Queries](manual.md) for instructions on how to view blocking activity and manually terminate it.
* [Setting the Lock Timeout](timeout.md) for configuring lock timeouts for migrations.
* [Advanced Configuration](advanced.md) for advanced usage such as creating custom actions to run when queries are blocked.

Core API information exists in these sections:

* [Settings](settings.md) for all available Django settings.
* [Release Notes](release_notes.md) for information about every release.
* [Contributing Guide](contributing.md) for details on contributing to the codebase.
