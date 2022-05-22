# bodyo_test

The Django app for the Nutrible Frontend.

## Installation

You will need `python3` with `virtualenv`. You'll also need some other miscellaneous dependencies (see `requirements/`), I think on the latest Ubuntu you'll need to run:

Clone the project to a folder and enter it:

```
git clone https://github.com/afnan-1/bodyo_test.git
```
## Virtuale Environment
python3 -m venv env
env/bin/activate

pip install -r requirements.txt

## Database Configuration
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```

```
python manage.py makemigrations
python manage.py migrate
```

## Run

```
python manage.py runserver
```
