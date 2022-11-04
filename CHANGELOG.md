# Changelog
## 1.0.1 (2022-11-03)
### Trivial
  - Bump the django-pglock requirement for Postgres<14 and support non-Postgres databases. [Wesley Kendall, 7fbd2c7]

## 1.0.0 (2022-10-25)
### Api-Break
  - V1 of ``django-pgmigrate`` [Wesley Kendall, 304246d]

    ``django-pgmigrate`` helps you avoid costly downtime with Postgres migrations
    and provides the following features to alleviate problematic locking
    scenarios when running migrations:

    * Detect blocking queries and terminate them automatically.
    * Print blocking queries so that you can inspect
      and terminate them manually.
    * Set the lock timeout so that migrations are terminated if they block too long.

