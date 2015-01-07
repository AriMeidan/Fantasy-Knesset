# Fantasy Knesset

This project is done in the framework of ["Hackita"](http://hackita.hasadna.org.il). It is a web site for creating your own Knesset, a fantasy Knesset, and to match it against the existing one.

## System description

Detailed description of the system, as well as future updates, are presented in the [following document](https://docs.google.com/document/d/1M4qsoHEYKac_bcuK7VAnTdIo1Q4wWOVshPqY1FRi0bk/edit?usp=sharing) (only Hebrew for now).

## Development

First, run the initial requirements and local database setup:

```bash
$ mkvirtualenv fknesset  # Using a Python virtualenv is highly recommended
$ pip install -r requirements.txt
$ python manage.py syncdb --migrate
```

Next, you can import some data using:

```bash
python manage.py populate_database
```

You now have a basic environment to work on :)

```bash
python manage.py runserver
```
