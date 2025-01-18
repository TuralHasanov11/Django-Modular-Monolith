```sh

# create virtual environment
python -m venv venv

# activate virtual environment
venv/scripts/activate 

# install packages
pip install -r requirements.txt

cd src

# copy the contents of .env.example file into .env file

python manage.py collectstatic --noinput

# check if any errors exist
python manage.py check

# run migrations
python manage.py makemigrations
python manage.py migrate

# create super user
python manage.py createsuperuser

# create some categories and products in admin
```
