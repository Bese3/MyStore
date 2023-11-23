#!/usr/bin/python3
"""
This module renders the front page with random objects from database.
"""
from flask import Flask, jsonify, make_response
# from flask_cors import CORS
from mods.portifolio import Portfolio
from mods.book import Book
from mods.music import Music
from mods.hobby import Hobby
from mods import dbstorage
import random
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    dbstorage.close()


@app.route("/portfolios", strict_slashes=False)
def portfolio():
    """
    The function "portfolio" retrieves a random portfolio from
    a database and returns it as a JSON object.
    """
    all_portfolios = [i for i in dbstorage.all(Portfolio).values()]
    try:
        my_port = random.choice(all_portfolios)
    except IndexError:
        return jsonify({})
    response = make_response((my_port.to_json()))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/books", strict_slashes=False)
def book():
    """
    The function selects a random book from
    a list of all books and returns it as a JSON object."""
    all_books = [i for i in dbstorage.all(Book).values()]
    try:
        my_book = random.choice(all_books)
    except IndexError:
        return jsonify({})
    response = make_response((my_book.to_json()))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/musics", strict_slashes=False)
def music():
    """
    The function selects a random music from
    a list and returns it as a JSON object.
    """
    all_musics = [i for i in dbstorage.all(Music).values()]
    try:
        my_music = random.choice(all_musics)
    except IndexError:
        return jsonify({})
    response = make_response((my_music.to_json()))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/hobbies", strict_slashes=False)
def hobbies():
    """
    The function "hobbies" retrieves a random hobby from
    a database and returns it as a JSON object.
    """
    all_hobbies = [i for i in dbstorage.all(Hobby).values()]
    try:
        my_hobby = random.choice(all_hobbies)
    except IndexError:
        return jsonify({})
    response = make_response((my_hobby.to_json()))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run()
