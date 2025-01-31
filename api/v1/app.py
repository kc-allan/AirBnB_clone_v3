#!/usr/bin/python3
'''Creates the flask app API.
'''
from flask import Flask
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
# Enable CORS code for task 2
CORS(app, resources={'/api/v1/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_flask(exception):
    """
    Removes the current SQLAlchemy Session object after each request.
    """
    storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    """
    Return errmsg `Not Found`.
    """
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    HOST = '0.0.0.0' if getenv(
        'HBNB_API_HOST'
    ) is None else getenv('HBNB_API_HOST')
    PORT = '5000' if getenv(
        'HBNB_API_PORT'
    ) is None else getenv('HBNB_API_PORT')
    app.run(host=HOST, port=PORT, threaded=True)
