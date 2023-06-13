# import argparse
from flask import Flask
from routers import main

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(main.page, url_prefix='/')

# parser = argparse.ArgumentParser()
# parser.add_argument('--host', default='0.0.0.0', help='host address')
# parser.add_argument('--port', default='5000', help='port number')
# args = parser.parse_args()

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
