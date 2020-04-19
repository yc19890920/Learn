# -*- coding:utf-8 -*-

import os
import time
import sys
import traceback
from selenium import webdriver
# from pyvirtualdisplay import Display

"""
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.0/geckodriver-v0.19.0-linux64.tar.gz
tar -zxvf geckodriver-v0.19.0-linux64.tar.gz
mv geckodriver /usr/bin/geckodriver
export PATH=$PATH:/usr/bin/geckodriver
pip install pyvirtualdisplay

If it says Error: GDK_BACKEND does not match available displays then install pyvirtualdisplay:
"""

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../edm_web'))
SCRIPT = os.path.join(ROOT, 'script')

GeckoDriver_Path = '/usr/bin/geckodriver'
# GeckoDriver_Path = os.path.join(SCRIPT, "geckodriver")
GeckoDriver_Path = 'D:\geckodriver\geckodriver.exe'


def get_error_addrs(username, passwd, check_addrs=None):
    res = None
    if not check_addrs: return []
    try:
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        driver = webdriver.Firefox(executable_path=GeckoDriver_Path)
        driver.set_page_load_timeout(10) # 防止页面加载个没完

        # QQ邮箱登录界面
        driver.get("https://mail.qq.com/")

        # 切换iframe
        driver.switch_to.frame("login_frame")
        driver.find_element_by_id("switcher_plogin").click()

        elem_user = driver.find_element_by_name("u")
        elem_user.clear()
        elem_user.send_keys(username)

        elem_pwd = driver.find_element_by_name("p")
        elem_pwd.clear()
        elem_pwd.send_keys(passwd)
        elem_but = driver.find_element_by_id("login_button")
        # elem_pwd.send_keys(Keys.RETURN)
        elem_but.click()

        # 直接跳出所有frame
        driver.switch_to_default_content()
        time.sleep(0.1)

        # 点击写信
        elem_but_w = driver.find_element_by_id("composebtn")
        elem_but_w.click()

        #切换至右侧 主iframe
        main_Frame1 = driver.find_element_by_id("mainFrame")
        driver.switch_to_frame(main_Frame1)

        # 发件人
        time.sleep(1)
        driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]/div[2]/input''').send_keys(check_addrs)
        time.sleep(1)

        print dir(driver)

        count = 10
        while count:
            print '----------------', count
            _t = driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]''')
            errors = _t.find_elements_by_css_selector("div.addr_base.addr_error")
            res = [e.text for e in errors]
            if res: break
            count -= 1
            time.sleep(1)
        driver.refresh()
    except BaseException as  e:
        print >>sys.stderr, e
        print >>sys.stderr, traceback.format_exc()
    finally:
        # driver.quit()
        # display.stop()
        return res

############################################################
# 安全调用对象
def safe_call(fn, *args, **kwargs):
    try :
        return fn(*args, **kwargs)
    except Exception, e:
        # sys.stderr.write('call "%s" failure\n %s' % (fn.__name__, e.message))
        # sys.stderr.write(traceback.format_exc())
        print >>sys.stderr, 'call "%s" failure\n %s' % (fn.__name__, e.message)
        print >>sys.stderr, traceback.format_exc()
        return None

# 等待调用成功 (有超时时间)
def time_call(fn, *args, **kwargs):
    try_count=3
    while try_count > 0 :
        res = safe_call(fn, *args, **kwargs)
        if res is not None:
            return res
        print >>sys.stderr, 'try call "%s" count: %d' % (fn.__name__, try_count)
        # sys.stderr.write('try call "%s" count: %d' % (fn.__name__, try_count))
        try_count -= 1
        time.sleep(3)
    return


if __name__ == "__main__":
    # 用户名 密码
    username="2948906420@qq.com"
    passwd="lanlan13266734099"
    # username="1793302800@qq.com"
    # passwd="marxkarlmmx"
    check_addrs = "fdsg54ge10001@qq.com;fdsg54ge10002@qq.com;fdsg54ge10003@qq.com;fdsg54ge10004@qq.com;fdsg54ge10005@qq.com;fdsg54ge10006@qq.com;fdsg54ge10007@qq.com;fdsg54ge10008@qq.com;fdsg54ge10009@qq.com;fdsg54ge10010@qq.com;fdsg54ge10011@qq.com;fdsg54ge10012@qq.com;fdsg54ge10013@qq.com;fdsg54ge10014@qq.com;fdsg54ge10015@qq.com;fdsg54ge10016@qq.com;fdsg54ge10017@qq.com;fdsg54ge10018@qq.com;fdsg54ge10019@qq.com;fdsg54ge10020@qq.com;fdsg54ge10021@qq.com;fdsg54ge10022@qq.com;fdsg54ge10023@qq.com;fdsg54ge10024@qq.com;fdsg54ge10025@qq.com;fdsg54ge10026@qq.com;fdsg54ge10027@qq.com;fdsg54ge10028@qq.com;fdsg54ge10029@qq.com;fdsg54ge10030@qq.com;fdsg54ge10031@qq.com;fdsg54ge10032@qq.com;fdsg54ge10033@qq.com;fdsg54ge10034@qq.com;fdsg54ge10035@qq.com;fdsg54ge10036@qq.com;fdsg54ge10037@qq.com;fdsg54ge10038@qq.com;fdsg54ge10039@qq.com;fdsg54ge10040@qq.com;fdsg54ge10041@qq.com;fdsg54ge10042@qq.com;fdsg54ge10043@qq.com;fdsg54ge10044@qq.com;fdsg54ge10045@qq.com;fdsg54ge10046@qq.com;fdsg54ge10047@qq.com;fdsg54ge10048@qq.com;fdsg54ge10049@qq.com;fdsg54ge10050@qq.com;fdsg54ge10051@qq.com;fdsg54ge10052@qq.com;fdsg54ge10053@qq.com;fdsg54ge10054@qq.com;fdsg54ge10055@qq.com;fdsg54ge10056@qq.com;fdsg54ge10057@qq.com;fdsg54ge10058@qq.com;fdsg54ge10059@qq.com;fdsg54ge10060@qq.com;fdsg54ge10061@qq.com;fdsg54ge10062@qq.com;fdsg54ge10063@qq.com;fdsg54ge10064@qq.com;fdsg54ge10065@qq.com;fdsg54ge10066@qq.com;fdsg54ge10067@qq.com;fdsg54ge10068@qq.com;fdsg54ge10069@qq.com;fdsg54ge10070@qq.com;fdsg54ge10071@qq.com;fdsg54ge10072@qq.com;fdsg54ge10073@qq.com;fdsg54ge10074@qq.com;fdsg54ge10075@qq.com;fdsg54ge10076@qq.com;fdsg54ge10077@qq.com;fdsg54ge10078@qq.com;fdsg54ge10079@qq.com;fdsg54ge10080@qq.com;fdsg54ge10081@qq.com;fdsg54ge10082@qq.com;fdsg54ge10083@qq.com;fdsg54ge10084@qq.com;fdsg54ge10085@qq.com;fdsg54ge10086@qq.com;fdsg54ge10087@qq.com;fdsg54ge10088@qq.com;fdsg54ge10089@qq.com;fdsg54ge10090@qq.com;fdsg54ge10091@qq.com;fdsg54ge10092@qq.com;fdsg54ge10093@qq.com;fdsg54ge10094@qq.com;fdsg54ge10095@qq.com;fdsg54ge10096@qq.com;fdsg54ge10097@qq.com;fdsg54ge10098@qq.com;fdsg54ge10099@qq.com;fdsg54ge10100@qq.com;"
    # check_addrs = "1248644045@qq.com;1@qq.com;"
    # check_addrs = "fdsg54ge10001@qq.com;fdsg54ge10002@qq.com;fdsg54ge10003@qq.com;fdsg54ge10004@qq.com;fdsg54ge10005@qq.com;fdsg54ge10006@qq.com;fdsg54ge10007@qq.com;fdsg54ge10008@qq.com;"
    t1 = time.time()
    res = time_call(get_error_addrs, username, passwd, check_addrs)
    print res
    print '-------------------', time.time() - t1
