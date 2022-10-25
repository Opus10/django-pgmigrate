.. _automatic:

Automatically Terminating Blocking Queries
==========================================

After :ref:`installation` of ``django-pgmigrate``, queries that
block migrations will be automatically terminated by default.

Here's an example of what it looks like:

.. image:: static/terminate_blocking.png

There are two main differences in the above output versus the normal
``migrate`` output:

1. The first output line shows the Postgres process ID. This is useful for
   manually querying active blocking locks.
2. The yellow text shows when a blocking query was detected and terminated.
   In our case, a query was blocking auth migration 12.

.. tip::

   If you'd like to disable automatically terminating blocking queries, consult
   the :ref:`manual` or :ref:`advanced` sections.

How it Works
------------

Underneath the hood, the `django-pglock library <https://django-pglock.readthedocs.io>`__
is used to discover blocking locks and terminate them. Specifically, the
``pglock.prioritize`` decorator is applied to migrations. This decorator:

* Runs a background thread and periodically checks for blocking locks.
* Uses the ``pglock.models.BlockedPGLock`` proxy model, which uses
  Postgres's `pg_blocking_pids function <https://www.postgresql.org/docs/current/functions-info.html>`__ to accurately determine
  which queries are blocking migrations.

Consult the `django-pglock library docs <https://django-pglock.readthedocs.io>`__
for more information on how ``pglock.prioritize`` works.

How Queries are Terminated
--------------------------

Blocking queries are terminated using Postgres's `pg_terminate_backend function <https://www.postgresql.org/docs/9.3/functions-admin.html>`__.
Calling this Postgres function on a query will
result in a ``django.db.utils.OperationalError`` being raised in the
process executing the query. If the process was in a transaction, the
transaction will be rolled back.

Only Terminate Long-Running Queries
-----------------------------------

By default, all blocking queries are immediately terminated when discovered.
You can configure the underlying action to only terminate blocking queries based on their duration.
Do this in settings.py:

.. code-block:: python

   import pgmigrate

   PGMIGRATE_BLOCKING_ACTION = pgmigrate.Terminate(blocking_activity__duration__gte="5 seconds")

The ``pgmigrate.Terminate`` action takes filters that can be applied to the underlying
``pglock.models.BlockedPGLock`` queryset. In this case, we are filtering it by any blocking queries
that have been running longer than five seconds.

.. note::

   Remember, the background worker runs on a periodic interval that defaults to one second. Given
   our example above, this means blocking queries can run up to six seconds before being
   terminated.
