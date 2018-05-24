release: rm has_power.db || true && flask migrate_database
web: gunicorn app:app --log-file=logs.log
