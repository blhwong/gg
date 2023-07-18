# gg

### Setup
Setup venv
```
python3 -m venv env
```
Install requirements file
```
pip install -r requirements.txt
```
Create .env file and enter environment variables
```
cp dotenv.dist .env
```
Start redis (install via homebrew)
```
redis-server
```
### Running app
Example
```
python src/main.py -s tournament/patchwork/event/ultimate-singles -t "Patchwork Ultimate Singles Upset Thread" -sr u_Fluid-Daikon6706 -fm 10
```
Command helper
```
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
```
pytest
```
With coverage
```
coverage run --source=src -m pytest -v tests && coverage html
```
