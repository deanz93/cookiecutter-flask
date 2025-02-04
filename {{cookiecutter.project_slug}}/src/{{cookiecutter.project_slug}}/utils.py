import os
from flask import Flask
from {{cookiecutter.project_slug}}.models import Log
from .extensions import db


app = Flask(__name__, root_path=os.path.join(os.getcwd()),
            instance_relative_config=True)


# Logging function
def log_action(action, module_name=None):
    log_entry = Log(action=action, module_name=module_name)
    db.session.add(log_entry)
    db.session.commit()