from flask import Blueprint
from app.api.v1 import user, book, client, token, gitf


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    user.api.regsiter(bp_v1)
    book.api.regsiter(bp_v1)
    client.api.regsiter(bp_v1)
    token.api.regsiter(bp_v1)
    gitf.api.regsiter(bp_v1)
    return bp_v1
