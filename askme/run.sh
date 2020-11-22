rm -rf db.sqlite3
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py dbgen --users 100 --tags 100 --questions 1000 --qlikes 3000 --answers 10000 --alikes 17000
python3 manage.py runserver