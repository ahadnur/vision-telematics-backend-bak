import os

apps = [
    'customers',
    'orders',
    'engineers',
    'dispatch',
    'accounts',
    'products',
    'services',
    'stock',
    'settings',
    'utilities'
]

for app in apps:
    os.system(f'python manage.py startapp {app}')
