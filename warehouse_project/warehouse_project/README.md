# Use cmd to create virtual enviroment
python -m venv boxvenv 

# Use virtual enviroment
boxvenv\Scripts\activate
# Install all dependecies into venv
pip install -r requirements.txt

# Create project 
django-admin startproject Projectname
# Create app
python manage.py startapp appname
# run migrations to create databse
python manage.py makemigrations
python manage.py migrate
# create superuser to work with admin panel
python manage.py createsuper
# Start project
py manage.py runserver
# test code
python manage.py test
