import importlib
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from .models import Module

def load_modules(app):
    modules_dir = 'modules'
    apps = {}

    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name)
        if os.path.isdir(module_path) and os.path.exists(os.path.join(module_path, '__init__.py')):
            module_entry = Module.query.filter_by(name=module_name).first()
            if module_entry and module_entry.enabled:
                module = importlib.import_module(f'modules.{module_name}.modules')
                importlib.reload(module)
                if hasattr(module, 'register'):
                    app.register_blueprint(module.register())

    # Combine the main app with modules
    app.run = DispatcherMiddleware(app.run, apps)
