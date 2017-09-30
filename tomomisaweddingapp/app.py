# all the imports
import os
import psycopg2
from urllib.parse import urlparse, uses_netloc
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary.api
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__, instance_relative_config=True)
# app.config.from_object('config')
# app.config.from_pyfile('config.py')
app = Flask(__name__, instance_relative_config=True)

if app.debug:
    print('running in debug mode')
    app.config.from_object('instance.config-%s' % os.environ['FLASK_ENV'])
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    app.config.update(SECRET_KEY='development key')
else:
    print('NOT running in debug mode')
    app.config['CLOUDINARY_CLOUD_NAME'] = os.environ['CLOUDINARY_CLOUD_NAME']
    app.config['CLOUDINARY_API_KEY'] = os.environ['CLOUDINARY_API_KEY']
    app.config['CLOUDINARY_API_SECRET'] = os.environ['CLOUDINARY_API_SECRET']
    app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    app.config['USERNAME'] = os.environ['USERNAME']
    app.config['PASSWORD'] = os.environ['PASSWORD']
    app.config.update(SECRET_KEY=os.environ['SECRET_KEY'])

# DB setting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String(80))
#     url = db.Column(db.String(120))
#
#     def __init__(self, public_id, url):
#         self.public_id = public_id
#         self.url = url
#
#     def __repr__(self):
#         return '<Url %r>' % self.url


# Load default config and override config from an environment variable
# app.config.update(dict(
#     SECRET_KEY='development key',
#     DATABASE=os.path.join(app.root_path, 'tomomisaweddingapp.db')
# ))
# app.config.from_envvar('FLASK_SETTINGS', silent=True)

## Cloudinary setting

cloudinary.config(
  cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],
  api_key = app.config['CLOUDINARY_API_KEY'],
  api_secret = app.config['CLOUDINARY_API_SECRET']
)

def init_db():
    db.create_all()
    _db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        _db.cursor().execute(f.read())
    _db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def connect_db():
    """Connects to the specific database."""
    uses_netloc.append("postgres")
    url = urlparse(app.config["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, '_database'):
        g._database = connect_db()
    return g._database

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, '_database'):
        g._database.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(app.config['USERNAME'])
    print(app.config['PASSWORD'])
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_images'))
    return render_template('login.html', error=error)

@app.route('/')
def show_images():
    db = get_db()
    cur = db.cursor()
    cur.execute('select public_id, url from images order by id desc')
    images = cur.fetchall()
    return render_template('show_images.html', images=images)

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/_list')
def get_image_urls_json():
    db = get_db()
    cur = db.cursor()
    cur.execute('select url from images order by id desc')
    images = cur.fetchall()
    for image in images:
        ## http://res.cloudinary.com/tomomisawedding/image/upload/c_fill,h_150,w_100/sample.jpg
        l = [i[0] for i in images]
    return jsonify(images = l)

@app.route('/add', methods=['POST'])
def add_image():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    file_to_upload = request.files['file']
    if file_to_upload:
         upload_result = upload(file_to_upload)
         if "error" in upload_result:
             return redirect(url_for('temp')) #TODO : create error dialog

         url, options = cloudinary_url(upload_result['public_id'], format = "jpg", crop = "fill", width = 100, height = 150)
         cur = db.cursor()
         cur.execute('insert into images (public_id, url) values (?,?)', [upload_result['public_id'], url])
         cur.commit()
         flash('New entry was successfully posted')

    return redirect(url_for('show_images'))
