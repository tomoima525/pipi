# all the imports
import os
import sys
import tempfile
import psycopg2
from urllib.parse import urlparse, uses_netloc
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary.api
from flask_sqlalchemy import SQLAlchemy
import socketio

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    VideoMessage, AudioMessage, FileMessage
)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

## init
app = Flask(__name__, instance_relative_config=True)

if app.debug:
    print('running in debug mode')
    app.config.from_object('instance.config-%s' % os.environ['FLASK_ENV'])
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    app.config.update(SECRET_KEY='development key')
    channel_secret = app.config['LINE_CHANNEL_SECRET']
    channel_access_token = app.config['LINE_CHANNEL_ACCESS_TOKEN']
else:
    ## TODO: clean up setting
    print('NOT running in debug mode')
    app.config['CLOUDINARY_CLOUD_NAME'] = os.environ['CLOUDINARY_CLOUD_NAME']
    app.config['CLOUDINARY_API_KEY'] = os.environ['CLOUDINARY_API_KEY']
    app.config['CLOUDINARY_API_SECRET'] = os.environ['CLOUDINARY_API_SECRET']
    app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    app.config['USERNAME'] = os.environ['USERNAME']
    app.config['PASSWORD'] = os.environ['PASSWORD']
    app.config.update(SECRET_KEY=os.environ['SECRET_KEY'])
    channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# get channel_secret and channel_access_token from your environment variable
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# DB setting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## Cloudinary setting

cloudinary.config(
  cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],
  api_key = app.config['CLOUDINARY_API_KEY'],
  api_secret = app.config['CLOUDINARY_API_SECRET']
)

# wrap Flask application with engineio's middleware
sio = socketio.Server(async_mode='eventlet')
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

# Socket
# for debugging
@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

# @sio.on('client')
# def receive(sid, message):
#     print('received ', message)
#     sio.emit('notify', 'returned %s' % message)

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

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

## Handler for LINE chat bot
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    if text == '写真一覧':
        ## Show image list
        link = '写真一覧です https://tomomisa-wedding-1015.herokuapp.com/list'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=link))

# Image Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    else:
        sorry_text='画像以外は送れません、ごめんなさい!'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=sorry_text))
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        #tempfile_path = tf.name
        upload_result = upload(tf.name)
        if "error" in upload_result:
            error_text='送信が失敗しました、もう一度トライしてみて下さい!'
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=error_text))
            return

        url, options = cloudinary_url(upload_result['public_id'], format = "jpg", crop = "fill", width = 100, height = 150)
        db = get_db()
        cur = db.cursor()
        cur.execute('insert into images (public_id, url) values (%s,%s)' , (upload_result['public_id'], url))
        db.commit()

        # Emit value to client
        sio.emit('notify', 'updated')

        # Send successful message to Line
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='送信されました!'),
                TextSendMessage(text=url)
                ])

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
    cur.execute('select public_id from images order by id desc')
    images = cur.fetchall()
    #for public_id in images:
        ## http://res.cloudinary.com/tomomisawedding/image/upload/c_fill,h_150,w_100/sample.jpg
        #l = [i[0] for i in images]
    l = ['https://res.cloudinary.com/tomomisawedding/image/upload/c_pad,b_black,h_150,w_150/%s.jpg' % i[0] for i in images]
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
         cur.execute('insert into images (public_id, url) values (%s,%s)' , (upload_result['public_id'], url))
         db.commit()
         flash('New entry was successfully posted')
         # Emit value to client
         print(" posted ")
         sio.emit('notify', 'updated')
    return redirect(url_for('show_images'))
