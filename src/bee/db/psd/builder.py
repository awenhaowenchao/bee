from io import StringIO


class Builder():
    def __init__(self):
        self.query = StringIO("")
        self.args = []

    def reset(self):
        self.query = None
        if self.args != None:
            self.args = self.args[:0]

    def write(self, string):
        self.query.write(string)

    def write_strs(self, *strs):
        for i in strs:
            self.query.write(i)

    def value(self):
        return self.query.getvalue()

    def fmt_value(self):
        return self.query.getvalue().replace("?", "%s")
