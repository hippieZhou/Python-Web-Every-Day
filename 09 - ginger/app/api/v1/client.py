from flask import request

from app.libs.redprint import Redprint
from app.libs.enums import ClientTypeEnum
from app.validators.forms import ClientForm, UserEmailForm
from app.models.user import User
from app.libs.error import APIException
from app.libs.error_code import Success

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_MINA: __register_user_by_mina
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(
        form.nickname.data, form.account.data, form.secret.data)


def __register_user_by_mina():
    pass
