# ETIP - εxodus tracker investigation platform

[![Build Status](https://github.com/Exodus-Privacy/etip/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/Exodus-Privacy/etip/actions/workflows/main.yml) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Exodus-Privacy/etip.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Exodus-Privacy/etip/context:python)

ETIP is meant to ease investigations on tracker detection. For the moment, it offers few features:

* track all modifications on trackers
* detect rules collisions for both network and code signature

## Contribute to the identification of trackers

If you wish to help us identify new trackers, you can **request an ETIP account** by sending a username and an email address to etip@exodus-privacy.eu.org

You can also take a look at to the following repositories:

* <https://github.com/YalePrivacyLab/tracker-profiles>
* <https://github.com/jawz101/potentialTrackers>

## Contributing to ETIP development

If you want to contribute to this project, you can refer to [this documentation](CONTRIBUTING.md).

## API

An API is available to help administrate the ETIP database.

### Authenticate

```sh
POST /api/get-auth-token/
```

Example:

```sh
curl -X POST http://localhost:8000/api/get-auth-token/ --data "username=admin&password=testtest"
```

You need to include your token as an `Authorization` header in all subsequent requests.

### Get trackers

```sh
GET /api/trackers/
```

Example:

```sh
curl -X GET http://localhost:8000/api/trackers/ -H 'Authorization: Token <your-token>'
```

## Development environment

### Installation

Clone the project

```sh
git clone https://github.com/Exodus-Privacy/etip.git
```

Create the Python virtual env

```sh
cd etip
virtualenv venv -p python3
source venv/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Create the database

```sh
export DJANGO_SETTINGS_MODULE=etip.settings.dev
cd etip/
python manage.py migrate

# Import tracker definitions from the official instance of εxodus
python manage.py import_trackers

# Import predefined tracker categories
python manage.py import_categories
```

Create admin user

```sh
python manage.py createsuperuser
```

### Run the tests

```sh
export DJANGO_SETTINGS_MODULE=etip.settings.dev
python manage.py test
```

### Start the server

```sh
export DJANGO_SETTINGS_MODULE=etip.settings.dev
python manage.py runserver
```

### Useful commands

Some admin commands are available to help administrate the ETIP database.

#### Compare with Exodus

This command retrieves trackers data from an εxodus instance and looks for differences with trackers in the local database.

```sh
python manage.py compare_with_exodus
```

Note: for now, it only compares with local trackers having the flag `is_in_exodus`.

The default εxodus instance queried is the public one available at <https://reports.exodus-privacy.eu.org> (see `--exodus-hostname` parameter).
