from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.models.base import db
from flask import jsonify, g
from app.libs.error_code import DeleteSuccess

api = Redprint('user')

# 管理员
@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)
    pass


# 管理员
@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    pass


@api.route('', methods=['GET'])
@auth.login_required
def get_user(uid):
    uid = g.user.id
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)
    # from app.test import QiYue
    # return jsonify(QiYue())


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('', methods=['PUT'])
def update_user():
    return 'update'
