# ETIP - εxodus tracker investigation platform [![Build Status](https://travis-ci.org/Exodus-Privacy/etip.svg?branch=master)](https://travis-ci.org/Exodus-Privacy/etip)

ETIP is meant to ease investigations on tracker detection. For the moment, it offers few functionalities:
* track all modifications on trackers
* detect rules collisions for both network and code signature

## Contribute to the identification of trackers

If you wish to help us identify new trackers, you can request an ETIP account by sending a username and an email address to etip@exodus-privacy.eu.org

## Development environment

### Installation

Clone the project
```commandline
git clone https://github.com/Exodus-Privacy/etip.git
```
Create the Python virtual env
```commandline
cd etip
virtualenv venv -p python3.5
source venv/bin/activate
```
Install dependencies
```commandline
pip install -r requirements.txt
```
Create the database
```commandline
export DJANGO_SETTINGS_MODULE=etip.settings.dev
cd etip/
python manage.py migrate

# Import tracker definitions from the official instance of εxodus
python manage.py import_trackers

# Import predefined tracker categories
python manage.py import_categories
```
Create admin user
```commandline
python manage.py createsuperuser
```

### Run the tests

```commandline
export DJANGO_SETTINGS_MODULE=etip.settings.dev
python manage.py test
```

### Start the server

```commandline
export DJANGO_SETTINGS_MODULE=etip.settings.dev
python manage.py runserver
```

### Useful commands
Some admin commands are available to help administrate the ETIP database.

#### Compare with Exodus
This command retrieves trackers data from an Exodus instance and looks for differences with trackers in the local database.
```commandline
python manage.py compare_with_exodus
```
Note: for now, it only compares with local trackers having the flag `is_in_exodus`.

The default Exodus instance queried is the public one available at https://reports.exodus-privacy.eu.org (see `--exodus-hostname` parameter).
