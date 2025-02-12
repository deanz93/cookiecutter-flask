from modules.manager.models import Log

from .extensions import db


# Logging function
def log_action(action, module_id=None):
    log_entry = Log(action=action, module_id=module_id)
    db.session.add(log_entry)
    db.session.commit()

