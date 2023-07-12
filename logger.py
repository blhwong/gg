import logging
from datetime import datetime
from pytz import timezone, utc


fmt = 'datetime=%(asctime)s - name=%(name)s - level=%(levelname)s - msg=%(message)s'
date_format = '%Y-%m-%dT%H:%M:%S%Z'

t = datetime.now(tz=utc)
t = t.astimezone(timezone('US/Central'))
t = t.strftime('%Y-%m-%dT%H:%M')

logging.basicConfig(
    level=logging.DEBUG,
    format=fmt,
    datefmt=date_format,
    filename=f'logs/{t}_gg_logs.log',
    filemode='w',
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter(fmt, datefmt=date_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
