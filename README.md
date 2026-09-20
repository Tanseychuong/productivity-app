# Smart Personal Schedule

A Django web app for managing contacts, journal entries, notes and tasks.

## Stack
- Django 5, SQLite locally, PostgreSQL in production
- Bootstrap 5 templates, WhiteNoise for static files

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Importing data from the old JSON version
```bash
python manage.py import_json --dry-run
python manage.py import_json
```

## Structure
```
config/     project settings and root URLs
planner/    models, forms, views, templates, import command
static/     CSS
```

## License
MIT