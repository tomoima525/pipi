# Tomo misa wedding app

## Share Image Instantly

## development

```sh
pip install --editable .
export FLASK_APP=tomomisaweddingapp   //module name
export FLASK_DEBUG=1 // Debugging
flask initdb
flask run
```

## environment
flask 0.12

## dependencies
Cloudinary

Create `instance/config.py` and setup below:

```python
USERNAME = 'xxx'
PASSWORD = 'pass'
CLOUDINARY_CLOUD_NAME="xxx"  
CLOUDINARY_API_KEY="xxx"  
CLOUDINARY_API_SECRET="xxx"  
```
