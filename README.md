# vision-telematics-backend

## Project Tree

``` bash
.
├── apps
│   └── example # A django rest app
│       ├── api
│       │   ├── v1 # Only the "presentation" layer exists here.
│       │   │   ├── __init__.py
│       │   │   ├── serializers.py
│       │   │   ├── urls.py
│       │   │   └── views.py
│       │   ├── v2 # Only the "presentation" layer exists here.
│       │   │   ├── __init__.py
│       │   │   ├── serializers.py
│       │   │   ├── urls.py
│       │   │   └── views.py
│       │   └── __init__.py
│       ├── fixtures # Constant "seeders" to populate your database
│       ├── management
│       │   ├── commands # Try and write some database seeders here
│       │   │   └── command.py
│       │   └── __init__.py
│       ├── migrations
│       │   └── __init__.py
│       ├── templates # App-specific templates go here
│       ├── tests # All your integration and unit tests for an app go here.
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── models.py
│       ├── services.py # Your business logic and data abstractions go here.
│       ├── urls.py
│       └── views.py
├── common # An optional folder containing common "stuff" for the entire project
├── config
│   ├── settings.py
│   ├── asgi.py
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── deployments # Isolate Dockerfiles and docker-compose files here.
├── docs
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── deployment.md
│   ├── local-development.md
│   └── swagger.yaml
├── requirements
│   ├── common.txt # Same for all environments
│   ├── development.txt # Only for a development server
│   ├── local.txt # Only for a local server (example: docs, performance testing, etc.)
│   └── production.txt # Production only
├── static # Your static files
├── .env.example # An example of your .env configurations. Add necessary comments.
├── static # Your static files
├── .gitignore # https://github.com/github/gitignore/blob/main/Python.gitignore
├── entrypoint.sh # Any bootstrapping necessary for your application
├── manage.py
├── pytest.ini
└── README.md
```


Migration order:

settings --> engineer --> products --> orders --> services
