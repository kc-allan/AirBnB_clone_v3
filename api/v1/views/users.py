#!/usr/bin/python3
"""This Module defines routes for the Users API"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Get specific users"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    details = request.get_json()
    if not isinstance(details, dict):
        abort(400, "Not a JSON")
    if "email" not in details:
        abort(400, "Missing email")
    if "password" not in details:
        abort(400, "Missing password")
    user = User()
    for key, val in details.items():
        setattr(user, key, val)
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    details = request.get_json()
    if not isinstance(details, dict):
        abort(400, "Not a JSON")
    to_be_ignored = ['id', 'email', 'created_at', 'updated_at']
    for key, val in details.items():
        if key not in to_be_ignored:
            setattr(user, key, val)
    return jsonify(user.to_dict()), 200
