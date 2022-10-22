django-pgmigrate
================

``django-pgmigrate`` helps you avoid costly downtime with Postgres migrations.

Imagine the following happens:

1. A long-running task queries a model in a transaction and keeps the transaction open.
2. ``python manage.py migrate`` tries to change a field on the model.

Because of how Postgres queues locks, this common scenario causes **every**
subsequent query on the model to block until the query from 1) has finished.

``django-pgmigrate`` provides the following features to alleviate problematic locking
scenarios when running migrations:

* Detect blocking queries and terminate them automatically (the default behavior).
* Print blocking queries so that you can inspect
  and terminate them manually.
* Set the lock timeout so that migrations are terminated if they block too long.

Quick Start
-----------

After following the :ref:`installation` section, running
``python manage.py migrate`` will automatically terminate any blocking
queries. Here's an example of what it looks like:

.. image:: static/terminate_blocking.png

There are two additional outputs in the ``migrate`` command versus the original:

1. The first output line shows the Postgres process ID. This is useful for
   querying activity that's blocking the process.
2. The yellow text shows when a blocking query was detected and terminated.
   In our case, it was blocking auth migration 12.

You can configure ``django-pgmigrate`` to show blocked queries instead of automatically
killing them, and you can also set the lock timeout to automatically cancel migrations if
they block for too long.
See the next steps below for more details.

Compatibility
-------------

``django-pgmigrate`` is compatible with Python 3.7 - 3.10, Django 2.2 - 4.1, and Postgres 10 - 15.

Next Steps
----------

We recommend everyone first read:

* :ref:`installation` for how to install the library.

After this, there are several usage guides:

* :ref:`automatic` for more information on how blocking queries are automatically terminated.
* :ref:`manual` for instructions on how to view blocking activity and manually terminate it.
* :ref:`timeout` for configuring lock timeouts for migrations.
* :ref:`advanced` for advanced usage such as creating custom actions to run when queries are blocked.

Core API information exists in these sections:

* :ref:`settings` for all available Django settings.
* :ref:`release_notes` for information about every release.
* :ref:`contributing` for details on contributing to the codebase.
