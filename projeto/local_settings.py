from projeto.settings import BASE_DIR

SECRET_KEY = 'django-insecure-nagj+$4d&1wg4rm(g0dt4ot0ztnterc#34t_=$3et2q^e27979'

DEBUG = True

ALLOWED_HOSTS = ['*', ]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }