#!/usr/bin/python3
"""
user Hobby API
"""
from api.v1.collections import app_collection
from api.v1.collections.user import origin
from flask import make_response, abort, request
from mods.user import User
from mods.hobby import Hobby
from mods import dbstorage


@app_collection.route('/<user_id>/hobbies', strict_slashes=False,
                      methods=['GET'])
def get_hobbies(user_id):
    """
    The function `get_hobbies` retrieves hobbies associated
    with a user and returns them as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    hobbies = dbstorage.get_relation(Hobby, user_id, "hobbies")
    if hobbies is None:
        abort(404)
    response = make_response([i.to_json() for i in hobbies], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/hobbies/', strict_slashes=False,
                      methods=['POST'])
def post_hobbies(user_id):
    """
    The function `post_hobbies` creates a new hobby for a
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
    new_hobby = Hobby(**data)
    dbstorage.new(new_hobby)
    new_hobby.save()
    response = make_response(new_hobby.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/hobbies/<hobby_id>', strict_slashes=False,
                      methods=['DELETE'])
def delete_hobby(user_id, hobby_id):
    """
    The function deletes a hobby from the database
    based on the user_id and hobby_id provided.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    hobby = dbstorage.get(Hobby, hobby_id)
    if hobby is None:
        return abort(404)
    dbstorage.delete(hobby)
    dbstorage.save()
    response = make_response({'status': 'OK'}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/hobbies/<hobby_id>', strict_slashes=False,
                      methods=['PUT'])
def put_hobby(user_id, hobby_id):
    """
    The function `put_hobby` updates a hobby object with the
    provided data and returns the updated hobby as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    hobby = dbstorage.get(Hobby, hobby_id)
    if hobby is None:
        return abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    for k, v in request.get_json().items():
        if k not in ig_keys:
            setattr(hobby, k, v)
    hobby.save()
    response = make_response(hobby.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response
