# Cooknomics

### Contributing

This short tutorial assumes you have already installed Python, virtualenv, Django etc.
Note that steps related to installing PostgreSQL are optional as SQLite can also be used for development.

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

If you use PyCharm, go to File -> Settings -> Project: Cooknomics -> Project Interpreter. Otherwise use pip. Install following packages:

```
psycopg2
autoslug
```

Clone the repo:

```
git clone https://github.com/mihal277/Cooknomics.git
```

Create a standard settings.py file and change the detabase setting into:

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

Also, let Django know about any apps used in the project, e.g:

```Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'videos'
]
```

Finish by making migrations in Django.

After making some changes, push the branch and start a new pull request.




### Docs (in Polish):

1. [Specyfikacja ogólna](https://docs.google.com/document/d/1n9y66y2N_7tTQVqIJG90byW1PNnvo9r_IjUtjLXqby0/edit?usp=sharing)
2. [Usecase'y](https://docs.google.com/document/d/1VePjd6CFBpNj6oXDiueuRqSyV8FtM03lg1_Le045E1U/edit)
3. [Plan zapewnienia jakości](https://docs.google.com/document/d/13xBvUBlO6ya9ITbzPrt9hIe-BiOwjhwksWscliNyaQQ/edit)

