from flask import Blueprint, jsonify, request
{% if cookiecutter.use_swagger == 'y' %}from flasgger import swag_from{% endif %}

bp = Blueprint('views', __name__)

@bp.route('/')
{% if cookiecutter.use_swagger == 'y' %}@swag_from({
    'responses': {
        200: {'description': 'Welcome message', 'examples': {'application/json': {'message': 'Welcome'}}}
    }
}){% endif %}
def index():
    return jsonify({"message": "Welcome to {{ cookiecutter.project_name }}"})

@bp.route('/api/v1/sum', methods=['POST'])
{% if cookiecutter.use_swagger == 'y' %}@swag_from({
    'parameters': [
        {'name': 'a', 'in': 'formData', 'type': 'integer', 'required': True},
        {'name': 'b', 'in': 'formData', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Sum result', 'examples': {'application/json': {'result': 5}}}
    }
}){% endif %}
def sum_numbers():
    a = int(request.form.get('a'))
    b = int(request.form.get('b'))
    return jsonify({'result': a + b})