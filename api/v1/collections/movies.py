#!/usr/bin/python3
"""
user hobby API
"""
from api.v1.collections import app_collection
from api.v1.collections.user import origin
from flask import make_response, jsonify, abort, request
from mods.user import User
from mods.movie import Movie
from mods import dbstorage


@app_collection.route('/<user_id>/movies', strict_slashes=False,
                      methods=['GET'])
def get_movies(user_id):
    """
    The function `get_movies` retrieves movies associated
    with a user and returns them as a JSON response.
    """
    movies = dbstorage.get_relation(Movie, user_id, "movies")
    if movies is None:
        abort(404)
    response = make_response([i.to_json() for i in movies], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/movies/', strict_slashes=False,
                      methods=['POST'])
def post_movie(user_id):
    """
    The function `post_movie` creates a new movie for a
    user and saves it in the database.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    if 'name' not in request.get_json():
        abort(400, description="name missing")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    data = {}
    for k, v in request.get_json().items():
        if k not in ig_keys:
            data[k] = v
    data['user_id'] = user_id
    new_movie = Movie(**data)
    dbstorage.new(new_movie)
    new_movie.save()
    response = make_response(new_movie.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/movies/<movies_id>', strict_slashes=False,
                      methods=['DELETE'])
def delete_movie(user_id, movie_id):
    """
    The function deletes a movie from the database
    based on the user_id and book_id provided.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    movie = dbstorage.get(Movie, movie_id)
    if movie is None:
        return abort(404)
    dbstorage.delete(movie)
    dbstorage.save()
    response = make_response({'status': 'OK'}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/movies/<movie_id>', strict_slashes=False,
                      methods=['PUT'])
def put_movie(user_id, movie_id):
    """
    The function `put_movie` updates a movie object with the
    provided data and returns the updated movie as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    movie = dbstorage.get(Movie, movie_id)
    if movie is None:
        return abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    for k, v in request.get_json().items():
        if k not in ig_keys:
            setattr(movie, k, v)
    movie.save()
    response = make_response(movie.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response
