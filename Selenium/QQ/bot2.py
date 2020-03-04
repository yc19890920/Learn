# encoding=utf-8
from selenium import webdriver
import time

# 启动chrome浏览器
driver = webdriver.Chrome()
# 进入qq邮箱登陆首页
driver.get("https://mail.qq.com/")
time.sleep(1)

# 窗口最大化
driver.maximize_window()
# 切换到登陆frame（!!!!!!!!必须先切换!!!!!!!!）
driver.switch_to.frame('login_frame')
driver.find_element_by_xpath("//*[@id='switcher_plogin']").click()
time.sleep(3)
#########登陆
# 输入用户名
username = driver.find_element_by_xpath("//*[@id='u']")
username.clear()
# 将xxxxxxxxxx换成qq邮箱账户
username.send_keys('xxxxxxxxxx')
# 输入密码：将1111111111替换为自己的邮箱密码
driver.find_element_by_id('p').send_keys('1111111111')
# 点击登陆
driver.find_element_by_id('login_button').click()
time.sleep(10)
# 断言登陆成功
assert '退出' in driver.page_source

#########写信
# 单击写信按钮
driver.find_element_by_link_text("写信").click()
time.sleep(2)
# 切换到mainFrame
driver.switch_to.frame('mainFrame')
time.sleep(2)
# 输入收件人
driver.find_element_by_xpath("//*[@id='toAreaCtrl']/div[2]/input").send_keys('123456789@qq.com')
# 输入主题
driver.find_element_by_id('subject').send_keys('test')
# 输入正文
o = driver.find_elements_by_class_name("qmEditorIfrmEditArea")
o[0].click()  # !!!!!!!must click!!!!!!!
o[0].send_keys("abc")

# 点击发送按钮
driver.find_element_by_xpath("//*[@id='toolbar']/div/a[1]").click()
time.sleep(3)
##driver.find_element_by_xpath('//a[@name="sendbtn" and @tabindex="9"]').click()
time.sleep(3)
# 断言发送成功
assert u"再写一封" in driver.page_source
# 关闭浏览器
driver.quit()