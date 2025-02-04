from flask import Blueprint, jsonify, request
{% if cookiecutter.use_swagger == 'y' %}from flasgger import swag_from
from .extensions import swagger{% endif %}


bp = Blueprint('views', __name__)


@bp.route('/')
{% if cookiecutter.use_swagger == 'y' %}@swag_from({
    'responses': {
        200: {'description': 'Welcome message', 'examples': {'application/json': {'message': 'Welcome'}}}
    }
}){% endif %}
def index():
    return jsonify({"message": "Welcome to {{ cookiecutter.project_name }}"})


{% if cookiecutter.use_swagger == 'y' %}@swagger.definition('Sum')
class Sum(object):
    """
    Sum Object
    ---
    properties:
        a:
            type: integer
        b:
            type: integer
    """
    def __init__(self, a, b):
        self.a = int(a)
        self.b = int(b)

    def dump(self):
        return dict(vars(self).items())
{% endif %}

@bp.route('/api/v1/sum', methods=['POST'])
def sum_numbers():
    {% if cookiecutter.use_swagger == 'y' %} """
    An endpoint for testing requestBody documentation.
    ---
    description: Post a request body
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Sum'
        required: true
    responses:
        200:
            description: The posted request body
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/Sum'
    """
    {% endif %}
    a = int(request.form.get('a'))
    b = int(request.form.get('b'))
    return jsonify({'result': a + b})