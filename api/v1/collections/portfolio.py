#!/usr/bin/python3
"""
user Portfolio API
"""
from api.v1.collections import app_collection
from api.v1.collections.user import origin
from flask import make_response, abort, request
from mods.user import User
from mods.portifolio import Portfolio
from mods import dbstorage


@app_collection.route('/<user_id>/portfolios', strict_slashes=False,
                      methods=['GET'])
def get_portfolios(user_id):
    """
    The function `get_portfolios` retrieves portfolios associated
    with a user and returns them as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    portfolios = dbstorage.get_relation(Portfolio, user_id, "portfolios")
    if portfolios is None:
        abort(404)
    response = make_response([i.to_json() for i in portfolios], 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/portfolios/', strict_slashes=False,
                      methods=['POST'])
def post_portfolio(user_id):
    """
    The function `post_portfolio` creates a new portfolio for a
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
    new_portfolio = Portfolio(**data)
    dbstorage.new(new_portfolio)
    new_portfolio.save()
    response = make_response(new_portfolio.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/portfolios/<portfolio_id>',
                      strict_slashes=False,
                      methods=['DELETE'])
def delete_portfolio(user_id, portfolio_id):
    """
    The function deletes a portifolio from the database
    based on the user_id and portfolio_id provided.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    portfolio = dbstorage.get(Portfolio, portfolio_id)
    if portfolio is None:
        return abort(404)
    dbstorage.delete(portfolio)
    dbstorage.save()
    response = make_response({'status': 'OK'}, 200)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response


@app_collection.route('/<user_id>/portfolios/<portfolio_id>',
                      strict_slashes=False,
                      methods=['PUT'])
def put_portfolio(user_id, portfolio_id):
    """
    The function `put_portfolio` updates a portfolio object with the
    provided data and returns the updated portfolio as a JSON response.
    """
    user = dbstorage.get(User, user_id)
    if user is None:
        abort(404)
    portfolio = dbstorage.get(Portfolio, portfolio_id)
    if portfolio is None:
        return abort(404)
    if not request.get_json():
        abort(400, description="Not supported type")
    ig_keys = ['id', 'created_at', 'updated_at', 'user_id']
    for k, v in request.get_json().items():
        if k not in ig_keys:
            setattr(portfolio, k, v)
    portfolio.save()
    response = make_response(portfolio.to_json(), 201)
    response.headers['Access-Control-Allow-Origin'] = origin
    return response
