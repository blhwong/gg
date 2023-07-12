import logging

fmt = 'datetime=%(asctime)s - name=%(name)s - level=%(levelname)s - msg=%(message)s'
date_format = '%Y-%m-%dT%H:%M:%S%Z'

logging.basicConfig(
    level=logging.DEBUG,
    format=fmt,
    datefmt=date_format,
    filename='logs/gg.log',
    filemode='w',
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter(fmt, datefmt=date_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
