# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Setup

```bash
pip install -r requirements.txt
python run.py
```

{% if cookiecutter.use_swagger == 'y' %}
Visit Swagger UI: http://localhost:5000/apidocs/
{% endif %}