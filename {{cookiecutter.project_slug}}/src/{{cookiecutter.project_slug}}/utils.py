from modules.manager.models import Log
from .extensions import db


# Logging function
def log_action(action, module_name=None):
    log_entry = Log(action=action, module_name=module_name)
    db.session.add(log_entry)
    db.session.commit()