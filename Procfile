release: service postgresql start && python manage.py create_db && python manage.py ingest
web: gunicorn run:app --log-file -