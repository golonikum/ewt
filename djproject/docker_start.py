#!/usr/bin/env python
# coding=utf-8
"""Wait for Postgres, create tables, load fixtures, then serve via gunicorn."""
import os
import sys
import time

_SCRIPT = os.path.abspath(__file__)
_HERE = os.path.dirname(_SCRIPT)
os.chdir(_HERE)
sys.path.insert(0, _HERE)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def wait_for_db():
    from django.db import connection
    last_error = None
    for _ in range(60):
        try:
            connection.cursor().execute("SELECT 1")
            return
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    sys.exit("Database not ready: %s" % last_error)


def ensure_admin():
    from django.contrib.auth.models import User
    username = os.environ.get("DJANGO_ADMIN_USER", "admin")
    password = os.environ.get("DJANGO_ADMIN_PASSWORD", "admin")
    email = os.environ.get("ADMIN_EMAIL", "admin@localhost")
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print("Created superuser %s" % username)


def main():
    wait_for_db()
    from django.core.management import call_command
    call_command("syncdb", interactive=False)
    try:
        call_command("loaddata", "core/fixtures/initial_data.json")
    except Exception as exc:
        print("loaddata skipped: %s" % exc)
    ensure_admin()
    workers = os.environ.get("GUNICORN_WORKERS", "3")
    os.execvp("gunicorn", [
        "gunicorn",
        "--bind", "0.0.0.0:8000",
        "--workers", workers,
        "--timeout", "30",
        "--access-logfile", "-",
        "--error-logfile", "-",
        "wsgi:application",
    ])


if __name__ == "__main__":
    main()
