import os
import cv2
import time
import uuid
import traceback
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from sys import platform

BASE_DIR = os.path.realpath(os.path.split(__file__)[0])
IMG_DIR = os.path.join(BASE_DIR, "tmp")

from utils.utils import log, LoginError, login_required, get_qq_captcha_code
from utils.eml import make_message


class QQRobot(object):
    LOGIN_URL = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/login?vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input24e6b9.css"

    def __init__(self, username, passwd, proxy_ip=None, proxy_port=None):
        """
        :param username:     用户名
        :param passwd:       密码
        :param proxy_ip:     访问QQ邮箱使用的IP, 为空是,默认选择本地IP
        :param proxy_port:   当IP不为空是, 通过端口port与IP通信, 默认为3128, 就是代理服务squid的默认端口
        """
        self.username = username
        self.passwd = passwd
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port or 31218
        self.is_login = False
        self.platform = platform
        if self.platform == "win32":
            self.geckopath = "F:\software\geckodriver\geckodriver.exe"
        else:
            self.geckopath = "/usr/bin/geckodriver"

    def refresh(self):
        log.info("refresh firefox, user: {}, proxy_ip: {}".format(self.username, self.proxy_ip))
        self.driver.refresh()

    def quit(self):
        log.info("quit user: {}, proxy_ip: {}".format(self.username, self.proxy_ip))
        try:
            self.driver.quit()
        except BaseException as e:
            log.info(e)
        if self.platform == "linux":
            try:
                self.display.stop()
            except BaseException as e:
                log.info(e)

    def login(self):
        self.set_driver()
        self.set_login()
        if self.set_login_check(timeout=1):
            return True

        self.set_login_verify()
        if self.set_login_check(timeout=3):
            return True
        self.quit()
        raise ValueError(u"不能登录QQ邮箱，重试")

    def set_profile(self):
        """ 设置代理 """
        profile = None
        if self.proxy_ip:
            profile = webdriver.FirefoxProfile()
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.http', self.proxy_ip)
            profile.set_preference('network.proxy.http_port', self.proxy_port)
            profile.set_preference('network.proxy.ssl', self.proxy_ip)
            profile.set_preference('network.proxy.ssl_port', self.proxy_port)
            profile.update_preferences()
        return profile

    def set_driver(self):
        """ 设置浏览器 """
        try:
            if self.platform == "linux":
                self.display = Display(visible=0, size=(800, 600))
                self.display.start()
            self.driver = webdriver.Firefox(executable_path=self.geckopath, firefox_profile=self.set_profile())
            self.driver.delete_all_cookies()
            # 防止页面加载个没完
            self.driver.set_page_load_timeout(300)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 30)

            # 设置初始登录页面
            self.driver.get(self.LOGIN_URL)
        except BaseException as e:
            self.quit()
            log.error(traceback.format_exc())
            raise LoginError("WebDriverException, can not set driver...")

    def set_login(self):
        """ 登录 """
        try:
            self.set_login_submit()
            # 断言登陆成功
            assert "退出" in self.driver.page_source
            # self.driver.find_element_by_xpath('''//div[@id="newVcodeIframe"]/iframe[1]''')
        except BaseException as e:
            try:
                log.info("login user: {}, retry login...".format(self.username))
                self.set_login_submit()
            except:
                pass

    def set_login_check(self, timeout=5):
        """ 检测是否已经登录 """
        index = 3
        while index:
            if self.driver.title.strip() == u"QQ邮箱":
                self.is_login = True
                return True
            index -= 1
            time.sleep(timeout)
        return False

    def set_login_submit(self):
        """ 登录提交 """
        self.driver.find_element_by_id("switcher_plogin").click()
        # self.wait.until(EC.presence_of_element_located((By.ID, 'u')))
        elem_user = self.driver.find_element_by_name("u")
        elem_user.clear()
        time.sleep(0.1)
        elem_user.send_keys(self.username)

        elem_pwd = self.driver.find_element_by_name("p")
        elem_pwd.clear()
        time.sleep(0.1)
        elem_pwd.send_keys(self.passwd)
        elem_but = self.driver.find_element_by_id("login_button")
        # elem_pwd.send_keys(Keys.RETURN)
        time.sleep(0.1)
        elem_but.click()

    def set_login_verify(self):
        """ 遇到验证码登录 """
        index = 3
        while index:
            try:
                time.sleep(0.5)
                log.info("get captcha_img user: {}, index: {}".format(self.username, index))
                newVcodeIframe = self.driver.find_element_by_xpath('''//div[@id="newVcodeIframe"]/iframe[1]''')
                self.driver.switch_to.frame(newVcodeIframe)

                captcha_img = self.set_login_save_img('capImg')
                rs, verify_code = get_qq_captcha_code(captcha_img)
                log.info(
                    'login user: {} captcha_img: {}, verifycode: {}'.format(self.username, captcha_img, verify_code))
                if not rs:
                    log.error('login user: {}, verify img fail'.format(self.username))
                    index -= 1
                    continue

                ele_verifycode = self.driver.find_element_by_id("capAns")
                ele_verifycode.send_keys(verify_code)
                self.driver.find_element_by_id("submit").click()
            except BaseException as e:
                log.error('user: %s, verifycode err, msg: %s' % (self.username, e))
                # log.error(traceback.format_exc())
                index -= 1
                if index == 1:
                    log.info("verify_login user: {}, retry login...".format(self.username))
                    self.set_login()

    def set_login_save_img(self, imgid, uid=None):
        """ 保存验证码 """
        if not uid:
            uid = str(uuid.uuid1())
        screenshot_img = os.path.join(IMG_DIR, "screenshot_{}.png".format(uid))
        captcha_img = os.path.join(IMG_DIR, "captcha_{}.png".format(uid))

        self.driver.save_screenshot(screenshot_img)
        img = self.driver.find_element_by_id(imgid)
        loc = img.location
        print("loc:")
        print(loc)

        image = cv2.imread(screenshot_img, True)
        # roi = image[int(loc['y']):int(loc['y']) + 40, int(loc['x']):int(loc['x']) + 138]
        roi = image[int(loc['y']):int(loc['y'])+48, int(loc['x']):int(loc['x'])+130]
        cv2.imwrite(captcha_img, roi)
        return captcha_img

    @login_required
    def check(self, addrs):
        res = None
        index = 3
        while index:
            try:
                if index == 2: self.refresh()
                if index == 1: time.sleep(5)
                # 直接跳出所有frame
                self.driver.switch_to.default_content()

                # 点击写信
                # self.wait.until(EC.presence_of_element_located((By.ID, 'composebtn')))
                elem_but_w = self.driver.find_element_by_id("composebtn")
                elem_but_w.click()

                # 切换至右侧 主iframe
                main_Frame1 = self.driver.find_element_by_id("mainFrame")
                self.driver.switch_to.frame(main_Frame1)

                # 发件人
                check_addrs = "{};1@qq.com;".format(addrs) if addrs else "1@qq.com;"
                self.driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]/div[2]/input''').send_keys(check_addrs)

                count = 30
                while count:
                    _t = self.driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]''')
                    errors = _t.find_elements_by_css_selector("div.addr_base.addr_error")
                    res = [e.text.strip().replace(";", "") for e in errors]
                    if res and res[-1] == '1@qq.com':
                        break
                    count -= 1
                    time.sleep(0.5)
                index = 0
            except BaseException as e:
                log.error('user: %s, check err, msg: %s' % (self.username, e))
                log.error(traceback.format_exc())
                index -= 1
        if res is None:
            self.is_login = False
        return res

    @login_required
    def send_email(self, addrs, subject, content, subtype="html"):
        try:
            self.driver.switch_to.default_content()

            # 点击写信
            # self.wait.until(EC.presence_of_element_located((By.ID, 'composebtn')))
            elem_but_w = self.driver.find_element_by_id("composebtn")
            elem_but_w.click()

            # 切换至右侧 主iframe
            main_Frame1 = self.driver.find_element_by_id("mainFrame")
            self.driver.switch_to.frame(main_Frame1)

            # 发件人
            self.driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]/div[2]/input''').send_keys(addrs)
            # 输入主题
            # self.driver.find_element_by_xpath('''//input[@id="subject"]''').send_keys(subject)
            self.driver.find_element_by_id('subject').send_keys(subject)
            # self.driver.find_element_by_xpath('''//input[@id="subject"]''').send_keys(subject)

            # 输入正文
            o = self.driver.find_elements_by_class_name("qmEditorIfrmEditArea")
            o[0].click()  # !!!!!!!must click!!!!!!!
            o[0].send_keys(content)

            time.sleep(1)

            # 点击发送按钮
            self.driver.find_element_by_xpath("//*[@id='toolbar']/div/a[1]").click()
            # driver.find_element_by_xpath('//a[@name="sendbtn" and @tabindex="9"]').click()

            time.sleep(3)
            # 断言发送成功
            assert "再写一封" in self.driver.page_source

        except:
            log.error("弹出验证框")
            self.refresh()
            return

            try:
                self.driver.switch_to.default_content()

                log.error("弹出验证框")
                # time.sleep(600)
                captcha_img = self.set_login_save_img('QMVerify_QMDialog_verify_img_code')
                rs, verify_code = get_qq_captcha_code(captcha_img)
                log.info(
                    'send email user: {} captcha_img: {}, verifycode: {}'.format(
                        self.username, captcha_img, verify_code))
                if not rs:
                    log.error('login user: {}, verify img fail'.format(self.username))
                    raise

                ele_verifycode = self.driver.find_element_by_id("QMVerify_QMDialog_verifycodeinput")
                ele_verifycode.send_keys(verify_code)
                self.driver.find_element_by_id("QMVerify_QMDialog_btnConfirm").click()

                time.sleep(3)
                assert "再写一封" in self.driver.page_source
            except:
                log.error(traceback.format_exc())
                self.is_login = False
                time.sleep(3600)
                # 关闭浏览器
                self.quit()


if __name__ == "__main__":
    v = QQRobot("2948906420@qq.com", "lanlan13266734099", None, None)
    v.login()
    # v.check("1248644045@qq.com,1@qq.com")

    while 1:
        subject, content, subtype = make_message()
        v.send_email("2948906420@qq.com", subject, content, subtype)
        log.info(subtype)
        log.info(subject)
        log.info(content)
        time.sleep(5)
