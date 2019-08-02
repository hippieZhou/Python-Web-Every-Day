from wtforms import Form
from app.libs.error_code import ParameterException
from flask import request


class BaseForm(Form):
    def __init__(self):
        # slice=True 当参数不能被序列化时不会爆异常
        data = request.get_json(slice=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
