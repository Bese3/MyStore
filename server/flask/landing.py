#!/usr/bin/python3
"""
This module renders the front page with random objects from database.
"""
from flask import Flask, jsonify, make_response
# from flask_cors import CORS
from mods.portifolio import Portfolio
from mods.book import Book
from mods import dbstorage
import random
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    dbstorage.close()


@app.route("/all", strict_slashes=False)
def all():
    """
    The function retrieves all portfolios and books from a database,
    randomly selects one of each, converts them to JSON format,
    and returns them in a response object.
    """
    all_portfolios = [i for i in dbstorage.all(Portfolio).values()]
    all_books = [i for i in dbstorage.all(Book).values()]
    all_dict = []
    try:
        my_port = random.choice(all_portfolios)
        all_dict.append(my_port.to_json())
    except IndexError:
        pass
    try:
        my_book = random.choice(all_books)
        all_dict.append(my_book.to_json())
    except IndexError:
        pass
    response = make_response(all_dict, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000)
