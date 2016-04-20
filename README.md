# Cooknomics

### Contributing

##### General hints

1. Try to always test every module. Use coverage.
2. Comment your code. Sphinx will be used to create documentation.
3. Use PEP 8 to maintain good coding style.


##### Making changes

1. Create a new branch.
2. Push the branch with your changes to the remote.
3. Create a new pull request for your code to be reviewed by at least one other collaborator.


##### How to install

This short tutorial assumes you have already installed Python, virtualenv, Django etc. 

It focuses primarily on installing and configuring PostgreSQL, which will be used in the final product.

Note that the steps related to installing PostgreSQL can actually be considered optional as SQLite is also suitable for development.


First, install and start PostgreSQL:

```
sudo apt-get install postgresql-9.4
sudo  service postgresql-9.4 initdb
sudo service postgresql-9.4 start
```

Creata a local database:

```
sudo  su - postgres
createdb cooknomics
createuser -P username
```

Find the file pg_hba.conf (path may vary) and modify it:

```
# "local" is for Unix domain socket connections only
local all all md5
# IPv4 local connections:
host all all 127.0.0.1/32 md5
# IPv6 local connections:
host all all ::1/128 md5
```

Install libpython3.5-dev:

```
sudo apt-get install libpython3.5-dev 
```

If you use PyCharm, go to File -> Settings -> Project: Cooknomics -> Project Interpreter. Otherwise use pip. Install the following packages:

```
psycopg2
autoslug
django-tinymce
coverage
requests
Sphinx
```

Clone the repo:

```
git clone https://github.com/mihal277/Cooknomics.git
```

Create a standard settings.py file and change the detabase settings into:

```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cooknomics',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

Also, let Django know about any apps used in the project. For now it's:

```Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'videos',
    'news',
    'tinymce',
    'coverage'
]
```

Unless you've made changes in models you don't have to create new migration files. If you did, however, type:

```
python manage.py makemigrations
```

Finish by telling Django to create or modify tables in your PostreSQL database:

```
python manage.py migrate
```

### Testing

##### How to write tests

Use coverage to determine what parts of your code are still not tested:
```
coverage run manage.py test -v 2
coverage html
```

Create or modify a specific file in app/tests folder.
If you've created a file, modify \_\_init.py\_\_ accordingly.

##### How to run tests

First, add this code to your setting.py file in order to use SQLite for testing, which is mucha faster:

```Python
import sys
if 'test' in sys.argv:
    DATABASES = {
        'default': {'ENGINE': 'django.db.backends.sqlite3'}
    }

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
    )
```

Now you can run coverage inside your virtualenv:
```
coverage run manage.py test whatever -v 2
```

### Documentation

##### Using Sphinx



### Docs (in Polish)

1. [Specyfikacja ogólna](https://docs.google.com/document/d/1n9y66y2N_7tTQVqIJG90byW1PNnvo9r_IjUtjLXqby0/edit?usp=sharing)
2. [Usecase'y](https://docs.google.com/document/d/1VePjd6CFBpNj6oXDiueuRqSyV8FtM03lg1_Le045E1U/edit)
3. [Plan zapewnienia jakości](https://docs.google.com/document/d/13xBvUBlO6ya9ITbzPrt9hIe-BiOwjhwksWscliNyaQQ/edit)

