- [Python Web自动化测试 Selenium ](https://juejin.im/post/5d592b88e51d456201486e37)



linux 下载geckodriver
```
apt-get update
apt-get install firefox
pip3 install selenium==3.0.2

https://github.com/mozilla/geckodriver/releases

wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz 
tar -C /opt -xzf ~/geckodriver-v0.26.0-linux64.tar.gz
chmod 755 /opt/geckodriver
ln -fs /opt/geckodriver /usr/bin/geckodriver 
ln -fs /opt/geckodriver /usr/local/bin/geckodriver

linux: 
    https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
windows: 
    https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip
```