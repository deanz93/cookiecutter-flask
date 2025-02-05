import importlib
import json
import os
import zipfile

from flask import current_app
from {{cookiecutter.project_slug}}.extensions import db
from .models import Module


def enable_module(module_name):
    from {{cookiecutter.project_slug}}.utils import log_action
    module_entry = Module.query.filter_by(name=module_name).first()

    if module_entry and not module_entry.enabled:
        importlib.import_module(f'modules.{module_name}.modules')
        module_entry.enabled = True
        db.session.commit()
        log_action("Enabled Module", module_name)
        return "Restarting Flask..."

def disable_module(module_name):
    from {{cookiecutter.project_slug}}.utils import log_action
    module_entry = Module.query.filter_by(name=module_name).first()
    if module_entry and module_entry.enabled:
        rules_to_remove = [rule for rule in current_app.url_map.iter_rules() if rule.endpoint.startswith(module_name)]
        for rule in rules_to_remove:
            current_app.url_map._rules.remove(rule)
            current_app.view_functions.pop(rule.endpoint, None)
        module_entry.enabled = False
        db.session.commit()
        log_action("Disabled Module", module_name)

def load_fixtures(module_path):
    fixtures_path = os.path.join(module_path, 'fixtures.json')
    if os.path.exists(fixtures_path):
        with open(fixtures_path) as f:
            data = json.load(f)
            for model_name, records in data.items():
                model_class = getattr(importlib.import_module(f'modules.{module_path.split("/")[-1]}.models'), model_name)
                for record in records:
                    db.session.add(model_class(**record))
            db.session.commit()

def install_module(zip_path):
    from {{cookiecutter.project_slug}}.utils import log_action
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('modules')
        extracted_dirs = [name for name in zip_ref.namelist() if '/' in name and '__init__.py' in name]
        if extracted_dirs:
            module_name = extracted_dirs[0].split('/')[0]
            module_entry = Module.query.filter_by(name=module_name).first()
            if not module_entry:
                module_entry = Module(name=module_name, enabled=True, version='1.0.0')
                db.session.add(module_entry)
                db.session.commit()
                load_fixtures(os.path.join('modules', module_name))
                log_action("Installed Module", module_name)