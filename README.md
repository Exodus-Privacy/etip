# ETIP - εxodus tracker investigation platform
ETIP is meant to ease investigations on tracker detection. For the moment, it offers few functionalities: 
* track all modifications on trackers
* detect rules collisions for both network and code signature

## Installation
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
cd etip/
python manage.py migrate
```
Start the server
```commandline
python manage.py runserver
```

## Import data
They are 2 commands:
* `python manage.py import_trackers` to import tracker definitions from the official instance of εxodus
* `python manage.py import_categories` to import predefined tracker categories
