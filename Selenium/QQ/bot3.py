# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
url = ("https://mail.qq.com/")
name = ("874**5483")
key = ("Zly1****612X")
out_name = ("65750**8@qq.com")
#
# 打开浏览器
driver.get(url)
driver.implicitly_wait(10)

# 最大化窗口
driver.maximize_window()

# 切换iframe
driver.switch_to.frame("login_frame")

# #定位至账号密码登录
# driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()

# #账号，密码输入
# driver.find_element_by_xpath('//*[@id="u"]').send_keys(name)
# driver.find_element_by_xpath('//*[@id="p"]').send_keys(key)

# #点击登录
# driver.find_element_by_xpath('//*[@id="login_button"]').click()

# 点击头像登录
driver.find_element_by_xpath('//*[@id="img_out_874335483"]').click()
time.sleep(5)

# 点击写信
driver.find_element_by_xpath('//*[@id="composebtn"]').click()
time.sleep(3)

# 切换iframe至写信
driver.switch_to.frame("mainFrame")
# driver.switch_to.frame(driver.find_element_by_id('mainFrame'))
time.sleep(3)

# 添加收件人
driver.find_element_by_xpath('//*[@id="toAreaCtrl"]/div[2]/input').send_keys(out_name)

# 添加主题
driver.find_element_by_xpath('//*[@id="subject"]').send_keys("TestCase1")

# 退出当前编辑Iframe
driver.switch_to.default_content()

# 切换Iframe至编辑正文
driver.switch_to.frame("mainFrame")
# Body_frame=driver.find_element_by_xpath('//iframe[@scrolling="auto"]')
Body_frame = driver.find_element_by_class_name("qmEditorIfrmEditArea")
driver.switch_to.frame(Body_frame)

# 添加正文
driver.find_element_by_xpath('/html/body').send_keys("I LOVE Python")
time.sleep(3)

# 退回大Frame再点击发送
driver.switch_to.parent_frame()
driver.find_element_by_xpath('//*[@id="toolbar"]/div/a[1]').click()