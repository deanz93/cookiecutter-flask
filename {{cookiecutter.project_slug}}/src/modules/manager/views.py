"""
This module provides functions for creating a new module and registering a subscription.

The create_module function creates a new module and sends a registration email. If the module
already exists, it sends the module a reminder email instead.

The register_subscription function registers a new subscription in the database.
"""
import importlib
import json
import os
import re
import shutil
import zipfile

from flask import current_app
from packaging.version import Version

from {{cookiecutter.project_slug}}.extensions import db
from {{cookiecutter.project_slug}}.utils import log_action

from .models import Module


def enable_module(module_name):
    """
    Enable a module.

    :param module_name: The name of the module to enable.

    :returns: A message indicating that the server is restarting.
    """
    module_entry = Module.query.filter_by(name=module_name).first()

    if module_entry and not module_entry.enabled:
        importlib.import_module(f'modules.{module_name}.modules')
        module_entry.enabled = True
        db.session.commit()
        log_action("Enabled Module", module_entry.id)
        return "Restarting Flask..."


def disable_module(module_name):
    """
    Disable a module.

    :param module_name: The name of the module to disable.

    :returns: None
    """
    module_entry = Module.query.filter_by(name=module_name).first()
    if module_entry and module_entry.enabled:
        rules_to_remove = [rule for rule in current_app.url_map.iter_rules() if rule.endpoint.startswith(module_name)]
        for rule in rules_to_remove:
            current_app.url_map._rules.remove(rule)
            current_app.view_functions.pop(rule.endpoint, None)
        module_entry.enabled = False
        db.session.commit()
        log_action("Disabled Module", module_entry.id)


def load_fixtures(module_path):
    """
    Load fixtures from a module's fixtures.json file into the database.

    :param module_path: The path to the module directory.

    :returns: None
    """
    fixtures_path = os.path.join(module_path, 'fixtures.json')
    if os.path.exists(fixtures_path):
        with open(fixtures_path, encoding='utf-8') as f:
            data = json.load(f)
            for model_name, records in data.items():
                module_name = module_path.split("/")[-1]
                model_module = importlib.import_module(f'modules.{module_name}.models')
                model_class = getattr(model_module, model_name)
                for record in records:
                    db.session.add(model_class(**record))
            db.session.commit()


def install_module(zip_path):
    """
    Install a module from a zip file.

    :param zip_path: The path to the zip file containing the module.

    :returns: None
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('modules')
        extracted_dirs = [name for name in zip_ref.namelist() if '/' in name and '__init__.py' in name]
        module_path = os.path.join('modules', extracted_dirs[0].split('/')[0])
        modules_json_path = os.path.join(module_path, 'modules.json')
        module_name = extracted_dirs[0].split('/')[0]
        if os.path.exists(modules_json_path):
            with open(modules_json_path, encoding='utf-8') as f:
                data = json.load(f)
                next_version = data['version']

                module_entry = Module.query.filter_by(name=data['name']).first()
                if module_entry:
                    current_version = module_entry.version
                    if Version(next_version) > Version(current_version):
                        shutil.rmtree(module_path)
                        module_entry.version = data['version']
                        db.session.commit()
                        log_action(f"Updated Module {data['name']}", module_entry.id)
                        return
                    log_action(f"Module {data['name']} no changes.", module_entry.id)
                    return
                new_module = Module(name=data['name'], enabled=True, version=next_version)
                db.session.add(new_module)
                db.session.commit()
                load_fixtures(os.path.join('modules', module_name))
                log_action(f"Installed Module {data['name']}", new_module.id)
                return


def create_module(name):
    """
    Create a new module with the specified name.

    This function validates the module name, creates a directory and necessary
    boilerplate files for a new module, and sets up the module structure.

    Args:
        name (str): The name of the module in CamelCase format.

    Returns:
        None

    Usage:
        flask generate module --name ModuleName
    """

    if not re.match(r'^[A-Z][a-z]*([A-Z][a-z]*)*$', name):
        print(f"Error: '{name}' is not a valid module name. \
            Please use a valid one-word or two-word CamelCase format, e.g. 'MyModule'.")
        return
    module_name = name
    module_name_underscore = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    cur_dir = os.path.abspath(os.getcwd())
    path = os.path.join(cur_dir, 'modules', module_name_underscore)

    # Ensure the main path exists or create it
    if os.path.exists(path):
        module_exist = f"Module named '{name}' already exists"
        overwrite_question = "Overwriting will delete existing data. Do you want to proceed? (yes/no):"
        overwrite = input(f"{module_exist}. {overwrite_question}").strip().lower()
        if overwrite not in ('yes', 'y'):
            print("Operation cancelled.")
            return
        shutil.rmtree(path, ignore_errors=False, onerror=None)

    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created at: {path}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return

    # Define the files to be created
    main_files = ["__init__.py", "urls.py", "utils.py", "views.py", "models.py", "modules.py", "modules.json"]

    for file in main_files:
        file_path = os.path.join(path, file)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Add boilerplate content based on the file type
                if file == "__init__.py":
                    f.write("# This is the __init__.py file for this module\n")
                elif file == "admins.py":
                    f.write(
                        "# Define your admin views here\n"
                        "from flask_admin import BaseView, expose\n\n"
                    )
                elif file == "forms.py":
                    f.write(
                        "# Define your forms here\n"
                        "from wtforms import Form, StringField, validators\n\n"
                    )
                elif file == "urls.py":
                    blueprint_code = (
                        f"{module_name_underscore}_bp = Blueprint('{module_name_underscore}', "
                        f"__name__, url_prefix='/{module_name_underscore}')\n"
                    )
                    f.write(
                        "# Define your routes here\n"
                        "from flask import Blueprint, request, jsonify\n"
                        f"from {current_app.import_name}.extensions import swagger\n\n"
                        f"{blueprint_code}"
                    )
                elif file == "utils.py":
                    f.write("# Define your utility functions here\n")
                elif file == "views.py":
                    f.write(
                        "# Define your views here\n"
                        "from flask import render_template, request\n"
                    )
                elif file == "models.py":
                    f.write(
                        "# Define your models here\n"
                        "import uuid\n"
                        "\n"
                        "from sqlalchemy.sql import func\n"
                        "\n"
                        "from database.core import Mixin\n"
                        f"from {current_app.import_name}.extensions import db\n"
                        "\n\n"
                        f"class {module_name}(Mixin, db.Model):\n"
                        "\n"
                        f"    __tablename__ = '{module_name_underscore}'\n"
                        "\n"
                        "    id = db.Column(\n"
                        "        db.String(36),\n"
                        "        primary_key=True,\n"
                        "        default=lambda: str(uuid.uuid4())\n"
                        "    )\n"
                    )
                elif file == "modules.py":
                    f.write(
                        "# Register your blueprint here\n"
                        f"from .urls import {module_name_underscore}_bp\n\n\n"
                        "def register():\n"
                        f"    return {module_name_underscore}_bp\n"
                    )
                elif file == "modules.json":
                    data = {
                        "version": "1.0.0",
                        "name": module_name_underscore
                    }
                    json.dump(data, f, indent=4)
            print(f"File created: {file_path}")
        except Exception as e:
            print(f"Error creating file {file}: {e}")

    # Create the models folder and file
    models_folder = os.path.join(path, "templates")
    try:
        os.makedirs(models_folder, exist_ok=True)
        print(f"Models directory created at: {models_folder}")

        # Create the models file with capitalized name
        template_file_path = os.path.join(models_folder, f"{module_name_underscore}.html")
        with open(template_file_path, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html lang='en'>\n")
            f.write("<head>\n")
            f.write("    <meta charset='UTF-8'>\n")
            f.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
            f.write(f"    <title>{module_name_underscore}</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("    <h1>{module_name_underscore}</h1>\n")
            f.write("    <p>This is example texts.</p>\n")
            f.write("</body>\n")
            f.write("</html>\n")
        print(f"Models file created: {template_file_path}")
    except Exception as e:
        print(f"Error creating models folder or file: {e}")

    print("Module creation complete!")
