from .settings import *

# Exemple : utiliser SQLite pour aller plus vite en test
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

TEST_RUNNER = 'partnerB2B.runners.CustomTestRunner'
