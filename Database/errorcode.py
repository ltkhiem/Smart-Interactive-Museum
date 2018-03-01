class AccessError(Exception):
    def __init__(self, ex, args, key, index):
        self.args = ("error at index %s with key '%s' in args : %s" % (index, key, args),)

class GetError(Exception):
    def __init__(self, ex):
        self.args = ex.args

class KeyConflict(Exception):
    def __init__(self, key):
        self.args = ('Already exist key "%s"' % key,)

class AddError(Exception):
    def __init__(self, ex):
        self.args = ex.args

class KeyNotExist(Exception):
    def __init__(self, key):
        self.args = ('Not exist key "%s"' % key,)

class UpdateError(Exception):
    def __init__(self, ex):
        self.args = ex.args

class DeleteError(Exception):
    def __init__(self, ex):
        self.args = ex.args

class ClearError(Exception):
    def __init__(self, ex):
        self.args = ex.args
