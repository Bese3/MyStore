#!/usr/bin/python3
"""
user friend API
"""
from api.v1.collections import app_collection
from flask import make_response, jsonify, abort
from mods.user import User
from mods.friend import Friend
from mods import dbstorage
origin = "*"


@app_collection.route('/users', strict_slashes=False,
                      methods=['GET'])
def get_users():
    all_users = dbstorage.all(User).values()
    if all_users is None:
        abort(404)
    response = make_response([i.to_json() for i in all_users], 200)
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
