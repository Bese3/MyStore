#!/usr/bin/python3
"""
user Friend API
"""
from api.v1.collections import app_collection
from flask import make_response, abort, request
from mods.user import User
from mods.friend import Friend
from mods import dbstorage
origin = "*"  # used to allow `Access-Control-Allow-origin` header


@app_collection.route('/users', strict_slashes=False,
                      methods=['GET'])
def get_users():
    all_users = dbstorage.all(User).values()
    if all_users is None:
        abort(404)
    response = make_response([i.to_json() for i in all_users], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/user', strict_slashes=False,
                      methods=['POST'])
def post_user():
    """
    The function `post_user` creates a new user object with
    the given user_id and saves it to the database,
    and returns a JSON response with the user object.
    """
    if not request.get_json():
        abort(400, description="Not supported type")
    if 'email' not in request.get_json():
        abort(400, description="email missing")
    if 'password' not in request.get_json():
        abort(400, description="password missing")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    data = {}
    for k, v in request.get_json().items():
        if k not in ig_keys:
            data[k] = v
    new_user = User(**data)
    new_user.save()
    response = make_response(new_user.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/user', strict_slashes=False,
                      methods=['PUT'])
def put_user(user_id):
    """
    The function `put_user` updates a user object with
    the given user_id and saves it to the database,
    and returns a JSON response with the user object.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    data = {}
    print(request.get_json())
    for k, v in request.get_json().items():
        if k not in ig_keys:
            setattr(user, k, v)
    user.save()
    response = make_response(user.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route("/<user_id>/delete_account", strict_slashes=False,
                      methods=['DELETE'])
def delete_user(user_id):
    """
    The function `delete_user` deletes a user from the database and
    returns a response indicating whether the deletion was successful.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    dbstorage.delete(user)
    dbstorage.save()
    response = make_response({"Deleted": True}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/friends', strict_slashes=False,
                      methods=['GET'])
def get_friends(user_id):
    """
    The function `user_friends` retrieves a user's friends
    from a database and returns them as a JSON response.
    """
    user = dbstorage.get_relation(Friend, user_id, "friends")
    if user is None:
        abort(404)
    response = make_response([i.to_json() for i in user], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/friends/<friend_id>', strict_slashes=False,
                      methods=['POST'])
def post_friends(user_id, friend_id):
    """
    The function `post_friends` creates a new friend object with
    the given user_id and friend_id, saves it to the database,
    and returns a JSON response with the friend object.
    """
    new_dict = {
        'user_id': user_id,
        'friend_id': friend_id
    }
    my_friend = Friend(**new_dict)
    try:
        my_friend.friend_valid()
    except ValueError as e:
        abort(make_response({"error": e}), 400)

    dbstorage.new(my_friend)
    my_friend.save()
    response = make_response(my_friend.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/friends/<friend_id>', strict_slashes=False,
                      methods=['DELETE'])
def delete_friends(user_id, friend_id):
    """
    The function deletes a friend from the database
    based on the user_id and friend_id provided.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    friend = dbstorage.get(Friend, user_id)
    if friend is None:
        return abort(404)
    dbstorage.delete(friend)
    dbstorage.save()
    response = make_response({'status': 'OK'}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response
