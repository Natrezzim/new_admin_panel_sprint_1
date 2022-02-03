import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

include(
    'components/database.py',
    'components/application_definition.py',
    'components/password_validation.py',
    'components/internationalization.py',
)

STATIC_URL = '/static/'

INTERNAL_IPS = [os.environ.get('INTERNAL_IPS')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
