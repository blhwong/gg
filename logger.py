# import logging
import logging.handlers

LOG_FORMAT = 'datetime=%(asctime)s - name=%(name)s - level=%(levelname)s - msg=%(message)s'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%Z'
LOG_FILENAME = 'logs/gg_logs.log'
LOG_FILE_SIZE = 10 * 1024 * 1024

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    filename=LOG_FILENAME,
    filemode='a',
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

rotating_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=LOG_FILE_SIZE, backupCount=5)

formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
console_handler.setFormatter(formatter)

logger = logging.getLogger('')

logger.addHandler(console_handler)
logger.addHandler(rotating_handler)
