from pipi.app import app
import os
import eventlet
import eventlet.wsgi

#port = int(os.environ.get('PORT', 5000))
#app.run(host='127.0.0.1', port=port, debug=True)

eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
