class LimiterMock(object):
    def limit(self, _):
        def inner(func):
            return func
        return inner

class LoginManagerMock(object):
    def user_loader(self, func):
        return func
    def login_required(self, func):
        return func
    def login_user(self, func):
        return func
