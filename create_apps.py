import os

apps = [
    'sales',
    'installations',
    'purchasing',
    'orders',
    'accounts',
    'customer_care'
]

for app in apps:
    os.system(f'python manage.py startapp {app}')
