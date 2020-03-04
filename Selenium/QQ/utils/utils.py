import traceback
from .deathbycaptcha import SocketClient

class log:
    error = lambda e: print("error: {}".format(e))
    info = lambda e: print("info: {}".format(e))


class LoginError(Exception): pass


def login_required(fun):
    def login(self, *args, **kwargs):
        if not self.is_login:
            log.error("retry login......")
            self.login()
        if self.is_login:
            return fun(self, *args, **kwargs)
        return None

    return login

# --------------接口获取验证码---------------
def get_captcha_code(captcha_file_path):
    client = SocketClient('Shoufeng', 'Shoufeng#123')
    client.is_verbose = False

    print('Your balance is %s US cents' % client.get_balance())
    captcha = ''
    retry = 3
    i = 0
    while i < retry:
        try:
            captcha = client.decode(captcha_file_path)
            break
        except Exception as e:
            print('verify code exception')
            print(traceback.format_exc())
            i += 1

    if captcha:
        print('CAPTCHA solved: %s' % captcha['text'])
        return True, captcha['text']
    return False, 'no captcha'


def get_qq_captcha_code(captcha_file_path):
    rs, captcha_text = get_captcha_code(captcha_file_path)
    if rs and len(captcha_text) != 4:
        captcha_text = 'fail'
    return rs, captcha_text