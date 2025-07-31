# coding=utf-8
from .base import *

SECRET_KEY = 'h6a8)tm@#emr=o%866(ek)p%xlnd9_xmd8y_*2$5+@o7+)(tf#'
DEBUG = True

STATIC_URL = '/static/'
STATIC_ROOT = f'{ROOT_DIR}/staticfiles/'
STATICFILES_DIRS = [f'{BASE_DIR}/static']
