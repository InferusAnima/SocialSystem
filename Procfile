release: python manage.py makemigrations && python manage.py migrate
web: gunicorn SocialSystem.wsgi --log-file -
