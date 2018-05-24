release: flask reset_database && flask migrate_database
web: gunicorn app:app --log-file=logs.log
