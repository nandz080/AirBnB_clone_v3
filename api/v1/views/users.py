#!/usr/bin/python3
'''
Module that defines a new view for User objects
that handles all default RESTful API actions.
'''
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users_list():
    '''
    Retrieves the list of all User objects
    '''
    return jsonify(
        [user_obj.to_dict() for user_obj in storage.all(User).values()]
    )


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''
    Retrieves a User object based on user_id
    '''
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    else:
        return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''
    Deletes a User object based on user_id
    '''
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    else:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Creates a User
    '''
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user_obj = User(**data)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    Updates a User object based on user_id
    '''
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
