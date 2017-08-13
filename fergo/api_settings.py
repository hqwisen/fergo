# JSON API Rest Framework settings
# http://django-rest-framework-json-api.readthedocs.io/en/stable/usage.html#configuration

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}



# Model Settings

TASK_SETTINGS = {
    'name_max_length': 200
}

PROJECT_SETTINGS = {
    'name_max_length': 50
}

PROJECT_RELATION = {
    'owned': 1,
    'shared_admin': 2,
    'shared_readonly': 3
}

TASK_RELATION = {
    'owned': 1,
}

