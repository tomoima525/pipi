# Tomo misa wedding app

## Share Image Instantly

## development(run locally)
Install dependencies

```sh
pip install --editable .
```

Run
```sh
export FLASK_APP=tomomisaweddingapp   //module name
export FLASK_DEBUG=1 // Debugging
export FLASK_ENV=dev
flask initdb // initialize db. Required only first time
flask run
```

or

```
export FLASK_DEBUG=1 // Debugging
export FLASK_ENV=dev
flask initdb // initialize db. Required only first time
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

Create `instance/config-dev.py` and setup below:

```python
USERNAME = 'xxx'
PASSWORD = 'pass'
CLOUDINARY_CLOUD_NAME="xxx"  
CLOUDINARY_API_KEY="xxx"  
CLOUDINARY_API_SECRET="xxx"  
```
