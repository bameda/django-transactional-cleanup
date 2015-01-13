SECRET_KEY = "test"
DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.sqlite3',
    }
}

MIDDLEWARE_CLASSES = [
    # Common middlewares
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",

    # Only needed by django admin
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

INSTALLED_APPS = ["tests"]
