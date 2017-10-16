# Tomo misa wedding app

- Share Image using LineBotApi

![phone](./art/phone.png?raw=true)
![screen](./art/screen.png?raw=true)

## development(run locally)
1. Create `instance/config-dev.py` and setup below:

```python
USERNAME = 'xxx'
PASSWORD = 'pass'
CLOUDINARY_CLOUD_NAME="xxx"  
CLOUDINARY_API_KEY="xxx"  
CLOUDINARY_API_SECRET="xxx"  
DATABASE_URL="postgres:///xxx"
DATABASE_URL="postgres:///weddingdb" //requied at 3.Setup DB
LINE_CHANNEL_SECRET='xxx'
LINE_CHANNEL_ACCESS_TOKEN='xxx'
```

2. Install dependencies

- Setup Python dependencies

```sh
pip install --editable .
```

- Setup webpack

```sh
cd tomomisaweddingapp/static
npm i --save
npm build
```

3. Setup DB
- Install Postgres DB -> http://postgresapp.com/documentation/
- Create DB for the service

4. Run
- Run Without web socket

```sh
export FLASK_APP=tomomisaweddingapp   //module name
export FLASK_DEBUG=1 // Debugging
export FLASK_ENV=dev
flask initdb // initialize db and create table. Required only first time
flask run
```

- Run with web socket server

```sh
export FLASK_APP=tomomisaweddingapp   //module name
export FLASK_DEBUG=1 // Debugging
export FLASK_ENV=dev
flask initdb // initialize db and create table. Required only first time
python run.py
```

Access `http://localhost:5000` to access debug page(uploading image).

## production(HEROKU)
- Set up variables from HEROKU console's setting
- Set WEB_CONCURRENCY=3 to manage multiple worker process

```sh
heroku login
git push heroku master
heroku run flask initdb // initialize db and create table.. Required only first time
```

## environment
python python-3.6.2
flask 0.12.2
Cloudinary 1.8.0
socketio
postgres SQL

## Credits
[Kyosuke Inoue](https://github.com/kyoro) - Gave me great advice around saving images and FrontEnd jQuery. Thank you so much!

## License

This app is under Apache v2 License. However, I would be very happy if you let me know before you use this source code for wedding or other events.
Twitter: [Tomoaki Imai](https://twitter.com/tomoaki_imai)
Gmail: tomoima525@gmail.com

```
Copyright 2017 Tomoaki Imai

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
