web: gunicorn --bind :8000 ERP-Template.wsgi:application
worker: python3 manage.py rqworker default