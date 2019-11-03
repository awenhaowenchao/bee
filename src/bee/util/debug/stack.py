import sys
import os


def stack():
    return_str = ""
    f = sys._getframe()
    f = f.f_back  # first frame is detailtrace, ignore it
    while hasattr(f, "f_code"):
        code = f.f_code
        if return_str == "":
            return_str = "%s(%s:%s)" % (os.path.basename(code.co_filename),
                                        code.co_name,
                                        f.f_lineno)
        else:
            return_str = "%s(%s:%s)->" % (os.path.basename(code.co_filename),
                                          code.co_name,
                                          f.f_lineno) + return_str

        f = f.f_back
    print(return_str)
