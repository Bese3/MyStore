#!/usr/bin/python3
"""
user hobby API
"""
from api.v1.collections import app_collection
from api.v1.collections.user import origin
from flask import make_response, jsonify, abort, request
from mods.user import User
from mods.music import Music
from mods import dbstorage


@app_collection.route('/<user_id>/musics', strict_slashes=False,
                      methods=['GET'])
def get_musics(user_id):
    """
    The function `get_musics` retrieves musics associated
    with a user and returns them as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    musics = dbstorage.get_relation(Music, user_id, "musics")
    if musics is None:
        abort(404)
    response = make_response([i.to_json() for i in musics], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/musics', strict_slashes=False,
                      methods=['POST'])
def post_music(user_id):
    """
    The function `post_music` creates a new music for a
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
    new_music = Music(**data)
    dbstorage.new(new_music)
    new_music.save()
    response = make_response(new_music.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/musics/<music_id>', strict_slashes=False,
                      methods=['DELETE'])
def delete_music(user_id, music_id):
    """
    The function deletes a music from the database
    based on the user_id and music_id provided.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    music = dbstorage.get(Music, music_id)
    if music is None:
        return abort(404)
    dbstorage.delete(music)
    dbstorage.save()
    response = make_response({'status': 'OK'}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/musics/<music_id>', strict_slashes=False,
                      methods=['PUT'])
def put_music(user_id, music_id):
    """
    The function `put_music` updates a music object with the
    provided data and returns the updated music as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    music = dbstorage.get(Music, music_id)
    if music is None:
        return abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    for k, v in request.get_json().items():
        if k not in ig_keys:
            setattr(music, k, v)
    music.save()
    response = make_response(music.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response
