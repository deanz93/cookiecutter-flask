import os
import re
import textwrap

# Search for all models.py files in all folder
models_files = []
for root, dirs, files in os.walk(f"{os.getcwd()}"):
    for file in files:
        if file == 'models.py':
            models_files.append(os.path.join(root, file))

print(models_files)
# Extract class names from all models.py files
class_names = []
for models_file in models_files:
    with open(models_file, 'r', encoding='utf-8') as f:
        content = f.read()
        classes = re.findall(r'^class\s+(\w+)\(.*\):', content, re.MULTILINE)
        class_names.extend(classes)

# Update the __init__.py file
INIT_FILE = f"{os.getcwd()}/database/__init__.py"
with open(INIT_FILE, 'r+', encoding='utf-8') as f:
    content = f.readlines()

    # Ensure `from .base import db` is present and is the last import
    BASE_IMPORT = 'from my_flask_app.extensions import db\n'
    if BASE_IMPORT not in content:
        LAST_IMPORT_LINE = -1
        for i, line in enumerate(content):
            if line.startswith('from ') or line.startswith('import '):
                LAST_IMPORT_LINE = i

        if LAST_IMPORT_LINE == -1:
            content.insert(0, BASE_IMPORT)
        else:
            content.insert(LAST_IMPORT_LINE + 1, BASE_IMPORT)

    # Add import statements for all models.py files
    for models_file in models_files:
        import_path = models_file.replace('/app/', '').replace('/', '.').replace('\\', '.').replace('.py', '')
        MODELS_IMPORT = f'from {import_path} import {", ".join(class_names)}\n'

        if MODELS_IMPORT not in content:
            BASE_IMPORT_INDEX = content.index(BASE_IMPORT)
            content.insert(BASE_IMPORT_INDEX, MODELS_IMPORT)

    # Update __all__ list
    ALL_ARRAY_LINE = None
    for i, line in enumerate(content):
        if line.startswith('__all__'):
            ALL_ARRAY_LINE = i
            break

    if ALL_ARRAY_LINE is not None:
        all_list_start = ALL_ARRAY_LINE
        all_list_end = all_list_start
        while not content[all_list_end].strip().endswith("]"):
            all_list_end += 1

        all_items = []
        for line in content[all_list_start:all_list_end + 1]:
            items = line.strip().replace("__all__ = [", "").replace("]", "")
            items = items.replace('"', "").replace("'", "").split(",")
            items = [item.strip() for item in items if item.strip()]
            all_items.extend(items)

        if 'db' not in all_items:
            all_items.insert(0, 'db')
        for class_name in class_names:
            if class_name not in all_items:
                all_items.append(class_name)

        FORMATTED_ALL = textwrap.fill(
            f'__all__ = {all_items}',
            width=110,
            initial_indent="",
            subsequent_indent=" " * 11,
            break_long_words=False,
            break_on_hyphens=False,
        )

        content[all_list_start:all_list_end + 1] = [FORMATTED_ALL + "\n"]

    if BASE_IMPORT in content:
        BASE_IMPORT_INDEX = content.index(BASE_IMPORT)
        if BASE_IMPORT_INDEX + 1 < len(content) and content[BASE_IMPORT_INDEX + 1].strip() != "":
            content.insert(BASE_IMPORT_INDEX + 1, "\n")

    f.seek(0, 0)
    f.writelines(content)
    f.truncate()
