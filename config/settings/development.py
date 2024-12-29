import json

from .base import *


DEBUG = True


ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

# THIRD_PARTY_APPS.append('rest_framework_swagger')


DATABASES = json.loads(env.str('DATABASES'))
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
