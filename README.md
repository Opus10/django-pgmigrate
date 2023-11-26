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

## Installation

Install `django-pgmigrate` with:

    pip3 install django-pgmigrate

After this, add `pgactivity`, `pglock`, and `pgmigrate` to the `INSTALLED_APPS` setting of your Django project.

## Quick Start

After following the installation instructions, running `python manage.py migrate` will automatically terminate any blocking queries. Here's an example of what it looks like:

![Terminate Blocking](docs/static/terminate_blocking.png)

There are two additional outputs in the `migrate` command versus the original:

1. The first output line shows the Postgres process ID. This is useful for querying activity that's blocking the process.
2. The yellow text shows when a blocking query was detected and terminated. In our case, it was blocking auth migration 12.

You can configure `django-pgmigrate` to show blocked queries instead of automatically killing them, and you can also set the lock timeout to automatically cancel migrations if they block for too long. See the documentation section below for more details.

## Compatibility

`django-pgmigrate` is compatible with Python 3.8 - 3.12, Django 3.2 - 5.0, Psycopg 2 - 3, and Postgres 12 - 16.

## Documentation

[View the django-pgmigrate docs here](https://django-pgmigrate.readthedocs.io) to learn more about:

* How blocking queries are automatically terminated.
* Configuring the command to show blocking activity instead of terminating it, along with instructions on how to manually view and terminate activity.
* Configuring lock timeouts to automatically stop migrations if they block for too long.
* Advanced usage such as creating custom actions to run when queries are blocked.

## Contributing Guide

For information on setting up django-pgmigrate for development and contributing changes, view [CONTRIBUTING.md](CONTRIBUTING.md).

## Primary Authors

- [Wes Kendall](https://github.com/wesleykendall)
- [Paul Gilmartin](https://github.com/PaulGilmartin)
