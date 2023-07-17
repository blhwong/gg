# gg

### Setup
Setup venv
```commandline
python3 -m venv env
```
Install requirements file
```commandline
pip install -r requirements.txt
```
Create .env file and enter environment variables
```commandline
cp dotenv.dist .env
```
Start redis (install via homebrew)
```commandline
redis-server
```
### Running app
Example
```commandline
python src/main.py -s tournament/patchwork/event/ultimate-singles -t "Patchwork Ultimate Singles Upset Thread" -sr u_Fluid-Daikon6706 -fm 10
```
Command helper
```commandline
(env) ➜  gg (main) ✗ python src/main.py -h
usage: main.py [-h] [-s SLUG] [-t TITLE] [-sr SUBREDDIT] [-f FILE] [-fm FREQUENCY_MINUTES]

options:
  -h, --help            show this help message and exit
  -s SLUG, --slug SLUG
  -t TITLE, --title TITLE
  -sr SUBREDDIT, --subreddit SUBREDDIT
  -f FILE, --file FILE
  -fm FREQUENCY_MINUTES, --frequency_minutes FREQUENCY_MINUTES
```

### Running tests
```commandline
pytest
```
With coverage
```commandline
coverage run --source=src -m pytest -v tests && coverage html
```
