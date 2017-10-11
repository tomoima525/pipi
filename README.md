# Tomo misa wedding app

## Share Image Instantly

## development(run locally)
1. Create `instance/config-dev.py` and setup below:

```python
USERNAME = 'xxx'
PASSWORD = 'pass'
CLOUDINARY_CLOUD_NAME="xxx"  
CLOUDINARY_API_KEY="xxx"  
CLOUDINARY_API_SECRET="xxx"  
DATABASE_URL="postgres:///xxx"
```

2. Install dependencies

```sh
pip install --editable .
```

3. Run
Run Without web socket

```sh
export FLASK_APP=tomomisaweddingapp   //module name
export FLASK_DEBUG=1 // Debugging
export FLASK_ENV=dev
flask initdb // initialize db. Required only first time
flask run
```

or run with web socket server

```
export FLASK_DEBUG=1 // Debugging
export FLASK_ENV=dev
flask tomomisaweddingapp.initdb // initialize db. Required only first time
python run.py
```

## production(HEROKU)
heroku login
git push heroku master
heroku run flask initdb // initialize db. Required only first time

## environment
python python-3.6.2
flask 0.12.2
Cloudinary
postgres SQL
