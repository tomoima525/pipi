# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    DATABASE=os.path.join(app.root_path, 'tomomisaweddingapp.db')
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)

## Cloudinary setting

cloudinary.config(
  cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],
  api_key = app.config['CLOUDINARY_API_KEY'],
  api_secret = app.config['CLOUDINARY_API_SECRET']
)

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

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
    cur = db.execute('select public_id, url from images order by id desc')
    images = cur.fetchall()
    return render_template('show_images.html', images=images)

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/_list')
def get_image_urls_json():
    db = get_db()
    cur = db.execute('select url from images order by id desc')
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
    ## public_id is from Cloudinary
    ## TODO add Cloudinary upload logic
    public_id = request.form['id']
    if len(public_id) == 0:
        return redirect(url_for('temp'))
    url = cloudinary.CloudinaryImage("sample.jpg").build_url(width = 100, height = 150, crop = 'fill')
    db.execute('insert into images (public_id, url) values (?,?)',
                 [request.form['id'], url])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_images'))
