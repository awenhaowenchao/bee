# 定义Exception

class ConstError(TypeError):
    """
    常量类型检查错误
    """
    pass

class BeeError(Exception):
    pass


class CodedError(BeeError):

    def __init__(self, code: int = 0, message: str= None, detail: str = None): # real signature unknown
        self.code = code
        self.message = message
        self.detail = detail

    def __str__(self):
        if self.detail == None or self.detail == "":
            return "{}({})".format(self.message, self.code)

        return "{}({}): {}".format(self.message, self.code, self.detail)



