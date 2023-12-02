#!/usr/bin/python3
"""
user hobby API
"""
from api.v1.collections import app_collection
from api.v1.collections.user import origin
from flask import make_response, jsonify, abort, request
from mods.user import User
from mods.book import Book
from mods import dbstorage


@app_collection.route('/<user_id>/books', strict_slashes=False,
                      methods=['GET'])
def get_books(user_id):
    """
    The function `get_books` retrieves books associated
    with a user and returns them as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    books = dbstorage.get_relation(Book, user_id, "books")
    if books is None:
        abort(404)
    response = make_response([i.to_json() for i in books], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/books/', strict_slashes=False,
                      methods=['POST'])
def post_books(user_id):
    """
    The function `post_books` creates a new book for a
    user and saves it in the database.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    if 'name' not in request.get_json():
        abort(400, description="name missing")
    if 'author' not in request.get_json():
        abort(400, description="author name missing")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    data = {}
    for k, v in request.get_json().items():
        if k not in ig_keys:
            data[k] = v
    data['user_id'] = user_id
    new_book = Book(**data)
    dbstorage.new(new_book)
    new_book.save()
    response = make_response(new_book.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/books/<book_id>', strict_slashes=False,
                      methods=['DELETE'])
def delete_book(user_id, book_id):
    """
    The function deletes a book from the database
    based on the user_id and book_id provided.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    book = dbstorage.get(Book, book_id)
    if book is None:
        return abort(404)
    dbstorage.delete(book)
    dbstorage.save()
    response = make_response({'status': 'OK'}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/books/<book_id>', strict_slashes=False,
                      methods=['PUT'])
def put_book(user_id, book_id):
    """
    The function `put_book` updates a book object with the
    provided data and returns the updated book as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    book = dbstorage.get(Book, book_id)
    if book is None:
        return abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    for k, v in request.get_json().items():
        if k not in ig_keys:
            setattr(book, k, v)
    book.save()
    response = make_response(book.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response
