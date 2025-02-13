"""
This module provides a blueprint for managing modules.

It provides a web interface for managing (enabling/disabling) and installing modules.
"""

import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .models import Module, Log
from .views import enable_module, disable_module, install_module


module_blueprint = Blueprint('modules', __name__, template_folder='templates', url_prefix='/modules')


# Admin panel
@module_blueprint.route('/manager/', methods=['GET', 'POST'])
@login_required
def module():
    """
    The admin panel for managing modules.

    Provides a web interface for managing (enabling/disabling) and installing modules.
    """
    if request.method == 'POST':
        action = request.form.get('action')
        module_name = request.form.get('module')

        if action == 'enable':
            enable_module(module_name)
            flash(f'Module {module_name} successfully enabled!', 'success')
        elif action == 'disable':
            disable_module(module_name)
            flash(f'Module {module_name} successfully disabled!', 'success')
        elif action == 'upload':
            file = request.files['file']
            if file and file.filename.endswith('.zip'):
                filepath = os.path.join(os.path.abspath(os.getenv("UPLOAD_FOLDER", 'uploads')), file.filename)
                file.save(filepath)
                install_module(filepath)
                flash(f'Module {file.filename} installed successfully!', 'success')

        return redirect(url_for('modules.module'))

    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('auth.login'))

    modules = Module.query.all()
    logs = Log.query.order_by(Log.timestamp.desc()).limit(10).all()
    return render_template('manager.html', modules=modules, logs=logs)
