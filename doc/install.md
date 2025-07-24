# Getting Started

- [Installing your development environment](#installing-your-development-environment)

## Installing your development environment

You have different ways of setting up your development environment:

- [Docker](#docker-setup)
- [Manual](#manual-setup)

### Docker setup

#### Requirements

- docker
- docker-compose

#### Prepare your settings

Create the file  `etip/etip/settings/custom_docker.py` with the following content:

```bash
from .docker import *

# Overwrite any other settings you wish to
```

#### Run

```bash
echo uid=$(id -u) > .env
docker-compose up -d
# Once etip started, you can check its logs
docker-compose logs -f etip
```

When everything is up, Docker logs say `ETIP DB is ready.`.

The etip container automatically:

- Create the database
- Make migration
- Start ETIP

Don't forget to rebuild your image and refresh your container if there is any change with `docker-compose up -d --build`.

#### Aliases

You can use the command

```bash
docker-compose exec etip /entrypoint.sh "<command>"
```

to make actions, where `<command>` can be:

- `compare-with-exodus`: Looks for differences with εxodus and local trackers
- `compile-messages`: Compile the translation messages
- `create-db`: Create the database and apply migrations
- `create-user`: Create a Django user
- `make-messages`: Create the extracted translation messages
- `start-etip`: Start the web server
- `test`: Run tests

### Manual setup

This setup is based on a Debian 12 (Bookworm) configuration.

#### 1 - Install dependencies

```bash
sudo apt install git virtualenv build-essential libssl-dev libffi-dev python3-dev libxml2-dev libxslt1-dev libpq-dev pipenv
```

#### 2 - Clone the project

```bash
git clone https://github.com/Exodus-Privacy/etip.git
```

#### 3 - Create database and user

```bash
sudo su - postgres
psql
CREATE USER etip WITH PASSWORD 'etip';
CREATE DATABASE etip WITH OWNER etip;
\c etip
```

#### 4 - Set Python virtual environment and install dependencies

```bash
cd exodus
pipenv install --dev
```

#### 5 - Configure your instance

You can tweak your instance by changing [some settings](#configuring-your-local-instance).

Follow instructions to get AAS token [here](https://github.com/EFForg/apkeep/blob/master/USAGE-google-play.md).

Create the file  `etip/etip/settings/custom_dev.py` with the following content:

```bash
from .dev import *

# Overwrite any other settings you wish to
```

#### 6 - Create the DB schema

```bash
echo "DJANGO_SETTINGS_MODULE=etip.settings.custom_dev" > .env
# enter into python environment
pipenv shell

cd etip
python manage.py migrate --fake-initial
python manage.py migrate

# Import tracker definitions from the official instance of εxodus
python manage.py import_trackers

# Import predefined tracker categories
python manage.py import_categories
```

#### 7 - Create admin user

```bash
python manage.py createsuperuser
```

#### 8 - Start ETIP

You have to activate the virtual venv and `cd` into the same directory as `manage.py` file.

```bash
pipenv shell
cd etip

python manage.py runserver
```

Now browse [http://127.0.0.1:8000](http://127.0.0.1:8000)

#### 9 - Run the tests

```sh
python manage.py test
```

