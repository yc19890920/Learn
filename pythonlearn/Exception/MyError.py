

class MyErr(BaseException):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)
