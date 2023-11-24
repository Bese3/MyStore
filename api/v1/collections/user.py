from api.v1.collections import app_collection
from flask import make_response, jsonify, abort, request
from mods.user import User
from mods.friend import Friend
from mods.portifolio import Portfolio
from mods import dbstorage


@app_collection.route('/users', strict_slashes=False,
                      methods=['GET'])
def get_users():
    all_users = dbstorage.all(User).values()
    if all_users is None:
        abort(404)
    return make_response([i.to_json() for i in all_users], 200)                   


@app_collection.route('/<user_id>/friends', strict_slashes=False,
                      methods=['GET'])
def get_friends(user_id):
    """
    The function `user_friends` retrieves a user's friends
    from a database and returns them as a JSON response.
    """
    user = dbstorage.get_relation(Friend, user_id, "friends")
    if user_id is None:
        abort(404)
    print("user")
    print(user)
    return make_response([i.to_json() for i in user], 200)

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
    dbstorage.save()
    return make_response(my_friend.to_json(), 200)


@app_collection.route('/<user_id>/friends/<friend_id>', strict_slashes=False,
                      methods=['DELETE'])
def delete_friends(user_id, friend_id):
    """
    The function deletes a friend from the database
    based on the user_id and friend_id provided.
    """
    friend = dbstorage.get(Friend, user_id)
    if friend is None:
        return abort(404)
    dbstorage.delete(friend)
    dbstorage.save()
    return make_response({'status': 'OK'}, 201)
