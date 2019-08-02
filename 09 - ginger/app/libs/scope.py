class Scope(object):
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


# class AdminScope(Scope):
#     allow_module = ['v1.user']

#     def __init__(self):
#         pass


# 等价于上述的权限控制配置
class AdminScope(Scope):
    allow_api = ['v1.user+super_get_user', 'v1.user+super_delete_user']

    def __init__(self):
        self + UserScope()


# class UserScope(Scope):
#     forbidden = ['v1.user+super_get_user', 'v1.user+super_delete_user']

#     def __init__(self):
#         self + AdminScope()


# 等价于上述的权限控制配置
class UserScope(Scope):
    allow_api = ['v1.user+get_user', 'v1.user+delete_user']


def is_in_scope(scope, endpoint):
    # 动态创建对象
    scope = globals()[scope]()

    splits = endpoint.split('+')
    red_name = splits[0]

    # 注意检测顺序
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
