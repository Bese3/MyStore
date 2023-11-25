#!/usr/bin/python3
from flask import Flask, make_response
from api.v1.collections import app_collection
from flask_cors import CORS
from mods import dbstorage
app = Flask(__name__)
app.register_blueprint(app_collection)
# CORS(app, resource={})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    dbstorage.close()


@app.errorhandler(404)
def not_found(error):
    """
    The function `not_found` returns a response with
    a 404 error message if a resource is not found.
    """
    return make_response({'error': 'Not Found'}, 404)


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5001)
