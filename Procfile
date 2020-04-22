web: gunicorn codelnmain.wsgi
worker: celery -A codelnmain worker --beat --scheduler django --loglevel=info