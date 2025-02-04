# Cookiecutter Flask

[![Build Status](https://img.shields.io/github/actions/workflow/status/cookiecutter/cookiecutter-django/ci.yml?branch=master)](https://github.com/cookiecutter/cookiecutter-django/actions/workflows/ci.yml?query=branch%3Amaster)
[![Documentation Status](https://readthedocs.org/projects/cookiecutter-django/badge/?version=latest)](https://cookiecutter-django.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Cookiecutter Flask is a framework for jumpstarting
development Flask projects quickly.

- If you have problems with Cookiecutter Django, please open [issues](https://github.com/cookiecutter/cookiecutter-django/issues/new) don't send
  emails to the maintainers.

## Features

- For Flask 3.0
- Works with Python 3.10 - 3.13
- Optimized development settings
- Docker support using [docker-compose](https://github.com/docker/compose) for development (using [Nginx](http://nginx.org/)
- Run tests with unittest or pytest
- Customizable PostgreSQL version

## Optional Integrations

_These features can be enabled during initial project setup._

- Configuration for [Celery](https://docs.celeryq.dev)

## Constraints

- Only maintained 3rd party libraries are used.
- Uses PostgreSQL everywhere: 12 - 16.
- Environment variables for configuration.

## Support this Project!

This project is an open source project run by volunteers. You can sponsor us via GitHub Sponsors:

- Mohamad Najmuddin Bin Yusoff, Project Creator ([GitHub](https://github.com/deanz93)).

Projects that provide financial support to the maintainers:

## Usage

First, get Cookiecutter. Trust me, it's awesome:

```bash
    # pipx is strongly recommended.
    pipx install cookiecutter

    # If pipx is not an option,
    # you can install cookiecutter in your Python user directory.
    python -m pip install --user cookiecutter
```

Now run it against this repo:

```bash
    cookiecutter https://github.com/deanz93/cookiecutter-flask.git
```

You'll be prompted for some values. Provide them, then a Flask project will be created for you.

**Warning**: After this point, change all the default values to your own desired values.

Enter the project and take a look around:

```bash
    cd {project-slug}/
    ls

Create a git repo and push it there:

    git init
    git add .
    git commit -m "first commit"
    git remote add origin '[github repo url]'
    git push -u origin main
```

Now take a look at your repo. Don't forget to carefully look at the generated README.

For local development, you can run with docker or without docker.

## Releases

Need a stable release? You can find them at <https://github.com/deanz93/cookiecutter-flask/releases>

### Submit a Pull Request

We accept pull requests if they're small, atomic, and make our own project development
experience better.

## Awesome Contributors

![deanz93](https://avatars.githubusercontent.com/u/7959977?v=4){:height="124px" width="124px"}
