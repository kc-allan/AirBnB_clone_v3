#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify

@app_views.route('/api/v1/users', methods=['GET'])
def get_all_users():
    users = storage.all(User)
    return jsonify(users)
@app_views.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = storage.get(User, user_id)
    return user