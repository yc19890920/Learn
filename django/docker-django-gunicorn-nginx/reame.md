- [dockerizing-django-with-postgres-gunicorn-and-nginx](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
- [Docker部署 - Django+MySQL+uWSGI+Nginx](https://zhuanlan.zhihu.com/p/29609591)
- [使用docker构建部署django+mysql项目(docker-compose)](https://www.centos.bz/2017/09/%E4%BD%BF%E7%94%A8docker%E6%9E%84%E5%BB%BA%E9%83%A8%E7%BD%B2djangomysql%E9%A1%B9%E7%9B%AEdocker-compose/)
- [Docker setup for Django on MySQL](https://medium.com/@minghz42/docker-setup-for-django-on-mysql-1f063c9d16a0)


# Dockerizing Django with Mysql, Gunicorn, and Nginx

This is a step-by-step tutorial that details how to configure Django to run on Docker with Postgres. 
For production environments, we'll add on Nginx and Gunicorn. 
We'll also take a look at how to serve Django static and media files via Nginx.
## Dependencies:
```
Django v1.11.3
Docker v18.09.7
Python v2.7.15
```

## Project Setup
Create a new project directory along with a new Django project:
```
$ mkdir django-on-docker && cd django-on-docker
$ mkdir app && cd app
$ python3.8 -m venv env
$ source env/bin/activate
(env)$ pip install django==2.2.6
(env)$ django-admin.py startproject hello_django .
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```

## Docker
Install Docker, if you don't already have it, then add a Dockerfile to the "app" directory:
```
# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . usr/src/app/
```

So, we started with an Alpine-based Docker image for Python 3.8.0. We then set a working directory along with two environment variables:
PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)

Finally, we updated Pip, copied over the requirements.txt file, installed the dependencies, and copied over the Django project itself.
Review Docker for Python Developers for more on structuring Dockerfiles as well as some best practices for configuring Docker for Python-based development.
Next, add a docker-compose.yml file to the project root:
```
version: '3.7'

services:
  web:
    build: ./app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./app/:/usr/src/app/
    ports:
      - 8000:8000
    env_file:
      - ./.env.dev
```

### Update the SECRET_KEY, DEBUG, and ALLOWED_HOSTS variables in settings.py:
```
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
```

Then, create a .env.dev file in the project root to store environment variables for development:
```
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
```

Build the image:
$ docker-compose build

Once the image is built, run the container:
$ docker-compose up -d

Navigate to http://localhost:8000/ to again view the welcome screen.

Check for errors in the logs if this doesn't work via docker-compose logs -f.

## Postgres
To configure Postgres, we'll need to add a new service to the docker-compose.yml file, update the Django settings, and install Psycopg2.

First, add a new service called db to docker-compose.yml:
```
version: '3.7'

services:
  web:
    build: ./app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./app/:/usr/src/app/
    ports:
      - 8000:8000
    env_file:
      - ./.env.dev
    depends_on:
      - db
  db:
    image: postgres:12.0-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=hello_django
      - POSTGRES_PASSWORD=hello_django
      - POSTGRES_DB=hello_django_dev

volumes:
  postgres_data:
```

To persist the data beyond the life of the container we configured a volume. This config will bind postgres_data to the "/var/lib/postgresql/data/" directory in the container.

We also added an environment key to define a name for the default database and set a username and password.

We'll need some new environment variables for the web service as well, so update .env.dev like so:
```
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
```

Update the DATABASES dict in settings.py:
```
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}
```


Here, the database is configured based on the environment variables that we just defined. Take note of the default values.

Update the Dockerfile to install the appropriate packages required for Psycopg2:
```
# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . usr/src/app/
```

Add Psycopg2 to requirements.txt:
```
Django==2.2.6
psycopg2-binary==2.8.3
```


Build the new image and spin up the two containers:
$ docker-compose up -d --build

Run the migrations:
$ docker-compose exec web python manage.py migrate --noinput

Get the following error?

django.db.utils.OperationalError: FATAL:  database "hello_django_dev" does not exist
Run docker-compose down -v to remove the volumes along with the containers. Then, re-build the images, run the containers, and apply the migrations.
Ensure the default Django tables were created:

Add the DATABASE environment variable to .env.dev:
```
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

Test it out again:
Re-build the images
Run the containers
Try http://localhost:8000/
Despite adding Postgres, we can still create an independent Docker image for Django as long as the DATABASE environment variable is not set to postgres.
 To test, build a new image and then run a new container:

$ docker build -f ./app/Dockerfile -t hello_django:latest ./app
$ docker run -p 8001:8000 \
    -e "SECRET_KEY=please_change_me" -e "DEBUG=1" -e "DJANGO_ALLOWED_HOSTS=*" \
    hello_django python /usr/src/app/manage.py runserver 0.0.0.0:8000
  
You should be able to view the welcome page at http://localhost:8001.

## Gunicorn
Moving along, for production environments, let's add Gunicorn, a production-grade WSGI server, to the requirements file:

Django==2.2.6
gunicorn==19.9.0
psycopg2-binary==2.8.3

Since we still want to use Django's built-in server in development, create a new compose file called docker-compose.prod.yml for production:
```
version: '3.7'

services:
  web:
    build: ./app
    command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
    ports:
      - 8000:8000
    env_file:
      - ./.env.prod
    depends_on:
      - db
  db:
    image: postgres:12.0-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env.prod.db

volumes:
  postgres_data:
```

Bring down the development containers (and the associated volumes with the -v flag):
docker-compose down -v

Then, build the production images and spin up the containers:
$ docker-compose -f docker-compose.prod.yml up -d --build

Verify that the hello_django_prod database was created along with the default Django tables. 
Test out the admin page at http://localhost:8000/admin. The static files are not being loaded anymore. 
This is expected since Debug mode is off. We'll fix this shortly.

Again, if the container fails to start, check for errors in the logs via docker-compose -f docker-compose.prod.yml logs -f.


Update the file permissions locally:

$ chmod +x app/entrypoint.prod.sh
To use this file, create a new Dockerfile called Dockerfile.prod for use with production builds:
```
###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.0-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.0-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]
```

Here, we used a Docker multi-stage build to reduce the final image size.
 Essentially, builder is a temporary image that's used for building the Python wheels. 
 The wheels are then copied over to the final production image and the builder image is discarded.


Did you notice that we created a non-root user?
By default, Docker runs container processes as root inside of a container. 
This is a bad practice since attackers can gain root access to the Docker host if they manage to break out of the container.
If you're root in the container, you'll be root on the host.

Update the web service within the docker-compose.prod.yml file to build with Dockerfile.prod:

web:
  build:
    context: ./app
    dockerfile: Dockerfile.prod
  command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
  ports:
    - 8000:8000
  env_file:
    - ./.env.prod
  depends_on:
    - db
Try it out:

$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput


## Nginx
Next, let's add Nginx into the mix to act as a reverse proxy for Gunicorn to handle client requests as well as serve up static files.

Add the service to docker-compose.prod.yml:
```
nginx:
  build: ./nginx
  ports:
    - 1337:80
  depends_on:
    - web
```


Then, in the local project root, create the following files and folders:
```
└── nginx
    ├── Dockerfile
    └── nginx.conf
```

Dockerfile:
```
FROM nginx:1.17.4-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
```

nginx.conf:
```
upstream hello_django {
    server web:8000;
}

server {

    listen 80;

    location / {
        proxy_pass http://hello_django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

}
```

Then, update the web service, in docker-compose.prod.yml, replacing ports with expose:
```
web:
  build:
    context: ./app
    dockerfile: Dockerfile.prod
  command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
  expose:
    - 8000
  env_file:
    - ./.env.prod
  depends_on:
    - db
```
Now, port 8000 is only exposed internally, to other Docker services. The port will no longer be published to the host machine.

Test it out again.

$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput


Ensure the app is up and running at http://localhost:1337.
Your project structure should now look like:
```
├── .env.dev
├── .env.prod
├── .env.prod.db
├── .gitignore
├── app
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── entrypoint.prod.sh
│   ├── entrypoint.sh
│   ├── hello_django
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.prod.yml
├── docker-compose.yml
└── nginx
    ├── Dockerfile
    └── nginx.conf
```

Bring the containers down once done:
$ docker-compose -f docker-compose.prod.yml down -v
Since Gunicorn is an application server, it will not serve up static files. So, how should both static and media files be handled in this particular configuration?

Static Files
Update settings.py:

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

Development
Collect the static files in entrypoint.sh:
```
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
```

Now, any request to http://localhost:8000/staticfiles/* will be served from the "staticfiles" directory.

To test, first re-build the images and spin up the new containers per usual. 
When the collectstatic command is run, static files will be placed in the "staticfiles" directory. 
Ensure static files are being served correctly at http://localhost:8000/admin.

Production
For production, add a volume to the web and nginx services in docker-compose.prod.yml so that each container will share a directory named "staticfiles":
```
version: '3.7'

services:
  web:
    build:
      context: ./app
      dockerfile: Dockerfile.prod
    command: gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/home/app/web/staticfiles
    expose:
      - 8000
    env_file:
      - ./.env.prod
    depends_on:
      - db
  db:
    image: postgres:12.0-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - ./.env.prod.db
  nginx:
    build: ./nginx
    volumes:
      - static_volume:/home/app/web/staticfiles
    ports:
      - 1337:80
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

We need to also create the "/home/app/web/staticfiles" folder in Dockerfile.prod:

...

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

...