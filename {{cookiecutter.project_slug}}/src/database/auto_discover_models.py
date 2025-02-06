import os
import re
from pathlib import Path
from collections import defaultdict

from modules.manager.models import Module


def auto_load_models(installed_apps):
    models_files = []
    enable_modules = get_enabled_modules()

    for module in enable_modules + installed_apps:
        module_path = os.path.join('modules', module, 'models.py')
        if os.path.exists(module_path):
            models_files.append(module_path)

    register_models(models_files)


def get_enabled_modules():
    enable_modules = []
    module_entry = Module.query.filter_by(enabled=True)
    for module in module_entry:
        enable_modules.append(module.name)
    return enable_modules


def register_models(models_files):
    root_project = Path(__file__).parent.parent

    # Extract class names from all models.py files, grouped by their file
    models_imports = defaultdict(list)
    for models_file in models_files:
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
            classes = re.findall(r'^(?!#\s*)class\s+(\w+)\(.*\):', content, re.MULTILINE)
            if classes:
                import_path = (
                    models_file.replace(str(root_project) + os.sep, '')
                    .replace('/', '.').replace('\\', '.')
                    .replace('.py', '')
                )
                models_imports[import_path].extend(classes)

    # Update the __init__.py file
    INIT_FILE = f"{root_project}/database/__init__.py"
    with open(INIT_FILE, 'r+', encoding='utf-8') as f:
        content = f.readlines()

        # Ensure `from {{cookiecutter.project_slug}}.extensions import db` is present
        BASE_IMPORT = 'from {{cookiecutter.project_slug}}.extensions import db\n'
        if BASE_IMPORT not in content:
            LAST_IMPORT_LINE = max(
                (i for i, line in enumerate(content) if line.startswith(('from ', 'import '))),
                default=-1
            )
            content.insert(LAST_IMPORT_LINE + 1 if LAST_IMPORT_LINE != -1 else 0, BASE_IMPORT)

        # Track existing imports
        existing_imports = {}
        for line in content:
            if line.startswith('from '):
                match = re.match(r'from (.+?) import (.+)', line)
                if match:
                    module, classes = match.groups()
                    existing_imports.setdefault(module.strip(), set()).update(
                        cls.strip() for cls in classes.split(',')
                    )

        # Add import statements for models, avoiding duplicates
        new_content = []
        inserted_modules = set()
        for line in content:
            if line.startswith('from ') and 'import' in line:
                module = line.split('import')[0].strip().replace('from ', '')
                if module not in inserted_modules:
                    inserted_modules.add(module)
                    new_content.append(line)
            else:
                new_content.append(line)

        # Insert new imports
        BASE_IMPORT_INDEX = new_content.index(BASE_IMPORT)
        for import_path, classes in models_imports.items():
            classes = sorted(set(classes))
            existing_classes = existing_imports.get(import_path, set())
            new_classes = set(classes) - existing_classes

            if new_classes:
                MODELS_IMPORT = f'from {import_path} import {", ".join(sorted(new_classes))}\n'
                new_content.insert(BASE_IMPORT_INDEX, MODELS_IMPORT)
                BASE_IMPORT_INDEX += 1

        # Update __all__ list
        all_items = set()
        for line in new_content:
            if line.startswith('__all__'):
                all_items.update(
                    item.strip("' \n")
                    for item in re.findall(r"'([^']+)'", line)
                )

        # Add 'db' and model classes to __all__
        all_items.add('db')
        for classes in models_imports.values():
            all_items.update(classes)

        # Replace or insert __all__
        all_list_line = next((i for i, line in enumerate(new_content) if line.startswith('__all__')), None)
        FORMATTED_ALL = f"__all__ = [{', '.join(f'\'{item}\'' for item in sorted(all_items))}]\n"

        if all_list_line is not None:
            new_content[all_list_line] = FORMATTED_ALL
        else:
            new_content.append('\n' + FORMATTED_ALL)

        # Write back to __init__.py
        f.seek(0)
        f.writelines(new_content)
        f.truncate()
