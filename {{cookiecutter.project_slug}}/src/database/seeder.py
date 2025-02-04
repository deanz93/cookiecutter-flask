import json
import os
import importlib
from pathlib import Path
from my_flask_app.extensions import db


# List of fixture file paths
FIXTURE_MAP = [
    "my_flask_app/fixtures/modules.json",
]


def load_json(file_path):
    """
    Loads JSON data from a file.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        list: The loaded JSON data, or an empty list if the file is not found or the JSON format is invalid.
    """
    try:
        root_project = Path(__file__).parent.parent
        fixture_path = os.path.join(root_project, file_path)
        with open(fixture_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Fixture file not found: {fixture_path}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in file: {fixture_path}. Error: {e}")
    return []


def find_model_class(class_name):
    """
    Dynamically searches and imports a model class within the src directory.

    Parameters:
        class_name (str): The name of the model class to find.

    Returns:
        class: The model class if found, otherwise None.
    """
    src_path = Path(__file__).parent.parent

    for root, _, files in os.walk(src_path):
        for file in files:
            if file == 'models.py':
                module_path = os.path.relpath(os.path.join(root, file), src_path)
                module_name = module_path[:-3].replace(os.path.sep, '.')

                try:
                    module = importlib.import_module(f'{module_name}')
                    if hasattr(module, class_name):
                        return getattr(module, class_name)
                except ImportError:
                    continue
    return None


def seed_database(replace=False):
    """
    Seeds the database with data from fixture files.

    Parameters:
        replace (bool): If True, clears existing data before seeding.

    Returns:
        None
    """
    for fixture_path in FIXTURE_MAP:
        data = load_json(fixture_path)

        for table_data in data:
            table_name = table_data.get('table')
            fields_list = table_data.get('fields', [])

            # Dynamically find the model class
            model = find_model_class(table_name)
            if not model:
                print(f"No model found for table: {table_name}")
                continue

            if replace:
                print(f"Clearing existing data for {table_name}...")
                db.session.query(model).delete()
                db.session.commit()
                print(f"Existing data for {table_name} cleared.")

            print(f"Seeding {table_name}...")
            objects = [model(**fields) for fields in fields_list]
            db.session.bulk_save_objects(objects)
            db.session.commit()
            print(f"Seeded {len(objects)} records for {table_name}.")

    print("Database seeded successfully.")
