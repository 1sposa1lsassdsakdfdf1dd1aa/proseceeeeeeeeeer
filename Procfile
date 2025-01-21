# Modify your app.py like this if needed:
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

if __name__ == '__main__':
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app)
    run_simple('0.0.0.0', 8080, app)
