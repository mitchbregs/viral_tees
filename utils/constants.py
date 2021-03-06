import os
import sys

from pathlib import Path


if sys.platform == 'darwin':
	SRC_DIR = Path(os.getcwd()).absolute()
elif sys.platform == 'linux2' or sys.platform == 'linux':
	SRC_DIR = Path('/home/git/viral_tees')
else:
	raise Exception('This system is not supported.')

##### DIRECTORIES

DATA_DIR = SRC_DIR / 'data'
LOG_DIR = SRC_DIR / 'logs'
STATIC_DIR = SRC_DIR / 'static'

TRENDS_DIR = DATA_DIR / 'trends'
TRIMMED_DIR = DATA_DIR / 'trimmed'
IMAGES_DIR = STATIC_DIR / 'images'
SHIRTS_DIR = DATA_DIR / 'shirts'
SHOPIFY_JSON = DATA_DIR / 'json'
RESPONSE_JSON = DATA_DIR / 'response'
TMP_DIR = DATA_DIR / 'tmp'


##### FILEPATHS

SHIRT_BG = STATIC_DIR / 'background.jpg'
ENV_PATH = SRC_DIR / '.env'