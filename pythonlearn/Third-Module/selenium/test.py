# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

"""
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.0/geckodriver-v0.19.0-linux64.tar.gz
tar -zxvf geckodriver-v0.19.0-linux64.tar.gz
mv geckodriver /usr/bin/geckodriver
export PATH=$PATH:/usr/bin/geckodriver
pip install pyvirtualdisplay


wget https://github.com/mozilla/geckodriver/releases/download/v0.10.0/geckodriver-v0.10.0-linux64.tar.gz
tar xzvf geckodriver-v0.10.0-linux64.tar.gz
cp geckodriver /usr/bin/
pip install selenium==3.0.0b3
"""
# 模拟登陆qq邮箱
geckoPath = 'D:\geckodriver\geckodriver.exe'
driver = webdriver.Firefox(executable_path=geckoPath)
driver.set_page_load_timeout(30) # 防止页面加载个没完

driver.get("https://mail.qq.com/")
driver.maximize_window()  #将浏览器最大化显示
time.sleep(2)

# 切换iframe
driver.switch_to.frame("login_frame")
driver.find_element_by_id("switcher_plogin").click()

# 用户名 密码
user="1248644045@qq.com"
passwd="lanlan1248644045"
user="1793302800@qq.com"
passwd="marxkarlmmx"
elem_user = driver.find_element_by_name("u")
elem_user.clear()
elem_user.send_keys(user)

elem_pwd = driver.find_element_by_name("p")
elem_pwd.clear()
elem_pwd.send_keys(passwd)
elem_but = driver.find_element_by_id("login_button")
# elem_pwd.send_keys(Keys.RETURN)
elem_but.click()

# 独立密码
# elem_pwd2 = driver.find_element_by_name("pp")
# elem_pwd2.send_keys("lan18924664854")
# elem_but2 = driver.find_element_by_id("btlogin")
# elem_but2.click()
# time.sleep(5)

# print driver.current_url

# 直接跳出所有frame
driver.switch_to_default_content()

elem_but_w = driver.find_element_by_id("composebtn")
elem_but_w.click()
# source = driver.page_source
# print source

#切换至右侧 主iframe
main_Frame1 = driver.find_element_by_id("mainFrame")
driver.switch_to_frame(main_Frame1)

# 发件人
time.sleep(30)
driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]/div[2]/input''').send_keys("493292335@qq.com;1@qq.com;2@qq.com;3@qq.com;")
time.sleep(60)

_t = driver.find_element_by_xpath('''//div[@id="toAreaCtrl"]''')
errors = _t.find_elements_by_css_selector("div.addr_base.addr_error")
for e in errors:
    print e.text


# # 主题
# driver.find_element_by_xpath("/html/body/form[2]/div[2]/div[3]/table[3]/tbody/tr[2]/td[2]/div/div/div/input").send_keys(u"lamw的信")
# time.sleep(10)
#
# # 正文
# o=driver.find_element_by_class_name("qmEditorIfrmEditArea")#难点2
# o.click()
# o.send_keys(u"hi，强，请查收附件")

driver.quit()