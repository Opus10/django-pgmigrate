# Changelog

## 1.5.0 (2024-11-01)

#### Changes

  - Added Python 3.13 support, dropped Python 3.8. Added Postgres17 support by [@wesleykendall](https://github.com/wesleykendall) in [#11](https://github.com/Opus10/django-pgmigrate/pull/11).

## 1.4.0 (2024-08-24)

#### Changes

  - Django 5.1 compatibilty, and Dropped Django 3.2 / Postgres 12 support by [@wesleykendall](https://github.com/wesleykendall) in [#10](https://github.com/Opus10/django-pgmigrate/pull/10).

## 1.3.1 (2024-04-06)

#### Trivial

  - Fix ReadTheDocs builds. [Wesley Kendall, e8807bc]

## 1.3.0 (2023-11-26)

#### Feature

  - Django 5.0 compatibility [Wesley Kendall, c884e46]

    Support and test against Django 5 with psycopg2 and psycopg3.

## 1.2.1 (2023-10-09)

#### Trivial

  - Added Opus10 branding to docs [Wesley Kendall, 7aa3296]

## 1.2.0 (2023-10-08)

#### Feature

  - Add Python 3.12 support and use Mkdocs for documentation [Wesley Kendall, d671a60]

    Python 3.12 and Postgres 16 are supported now, along with having revamped docs using Mkdocs and the Material theme.

    Python 3.7 support was dropped.

## 1.1.0 (2023-06-09)

#### Feature

  - Added Python 3.11, Django 4.2, and Psycopg 3 support [Wesley Kendall, 2f12991]

    Adds Python 3.11, Django 4.2, and Psycopg 3 support along with tests for multiple Postgres versions. Drops support for Django 2.2.

## 1.0.1 (2022-11-04)

#### Trivial

  - Bump the django-pglock requirement for Postgres<14 and support non-Postgres databases. [Wesley Kendall, 7fbd2c7]

## 1.0.0 (2022-10-25)

#### Api-Break

  - V1 of ``django-pgmigrate`` [Wesley Kendall, 304246d]

    ``django-pgmigrate`` helps you avoid costly downtime with Postgres migrations
    and provides the following features to alleviate problematic locking
    scenarios when running migrations:

    * Detect blocking queries and terminate them automatically.
    * Print blocking queries so that you can inspect
      and terminate them manually.
    * Set the lock timeout so that migrations are terminated if they block too long.
