# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

[![Built with Cookiecutter Flask](https://img.shields.io/badge/built%20with-Cookiecutter%20Flask-ff69b4.svg?logo=cookiecutter)](https://gitlab.plisca.net/plisca-ih/flask-boilerplate.git)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

## Basic Commands

### Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt
python run.py
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt
python -m pytest --cov=app --cov-report=html
open htmlcov/index.html
```

#### Running tests with pytest

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/local.txt
pytest
```

{%- if cookiecutter.use_celery == "y" %}

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -l info
```

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -B -l info
```

{%- endif %}
{%- if cookiecutter.use_docker == "y" %}

### Docker Setup

```bash
docker-compose up -d
```

{%- endif %}
{% if cookiecutter.use_swagger == 'y' %}
Visit Swagger UI: <http://localhost:5000/apidocs/>
{% endif %}