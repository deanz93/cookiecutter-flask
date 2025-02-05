from flasgger import swag_from
from flask import Blueprint, current_app, jsonify

bp = Blueprint('views', __name__)


@bp.route('/')
@swag_from({
    'responses': {
        200: {'description': 'Welcome message from Swagger {{ cookiecutter.project_name }}', 'examples': {'application/json': {'message': 'Welcome'}}}
    }
})
def index():
    return jsonify({"message": "Welcome to {{ cookiecutter.project_name }}"})


{% if cookiecutter.use_cloud_storage == 'y' %}@bp.route('/s3/')
def check_s3():
    s3_storage = current_app.extensions['s3_storage']
    response = s3_storage.list_objects(delimiter='/', prefix="/")
    return jsonify(response)
{% endif %}

@bp.route('/routes')
@swag_from({
    'responses': {
        200: {
            'description': 'List of routes',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'routes': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'endpoint': {'type': 'string'},
                                        'methods': {
                                            'type': 'array',
                                            'items': {'type': 'string'}
                                        },
                                        'url': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    },
                    'examples': {
                        'application/json': {
                            'routes': [
                                {
                                    'endpoint': 'example_endpoint',
                                    'methods': ['GET', 'POST'],
                                    'url': '/example/url'
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
})
def list_routes():
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'url': str(rule)
        })
    return jsonify({"routes": routes})
