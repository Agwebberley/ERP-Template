python3 manage.py makemigrations --noinput customers orders inventory finance core
python3 manage.py migrate
python3 manage.py update_config
python3 manage.py fake_data