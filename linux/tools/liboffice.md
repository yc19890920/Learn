安装包使用周工的安装包：
http://download.comingchina.com/temp/LibreOffice_6.1.5_Linux_x86-64_rpm.tar.gz
http://download.comingchina.com/temp/LibreOffice_6.1.5_Linux_x86-64_rpm_langpack_zh-CN.tar.gz
 
字体安装包：
http://download.comingchina.com/temp/yulan.zip




下载安装包  
wget -P /tmp/office http://mirrors.ustc.edu.cn/tdf/libreoffice/stable/6.1.3/rpm/x86_64/LibreOffice_6.1.3_Linux_x86-64_rpm.tar.gz
wget -P /tmp/office http://mirrors.ustc.edu.cn/tdf/libreoffice/stable/6.1.3/rpm/x86_64/LibreOffice_6.1.3_Linux_x86-64_rpm_langpack_zh-CN.tar.gz

解压缩
tar zxvf /tmp/office/LibreOffice_6.1.3_Linux_x86-64_rpm.tar.gz -C /tmp/office
tar zxvf /tmp/office/LibreOffice_6.1.3_Linux_x86-64_rpm_langpack_zh-CN.tar.gz -C /tmp/office


检查安装包
ll /tmp/office/LibreOffice_6.1.3.2_Linux_x86-64_rpm/RPMS/*.rpm
ll /tmp/office/LibreOffice_6.1.3.2_Linux_x86-64_rpm_langpack_zh-CN/RPMS/*.rpm

用yum安装，不要执行install
yum install /tmp/office/LibreOffice_6.1.3.2_Linux_x86-64_rpm/RPMS/*.rpm
yum install /tmp/office/LibreOffice_6.1.3.2_Linux_x86-64_rpm_langpack_zh-CN/RPMS/*.rpm


安装libcairo.so.2依赖库
yum install ibus


查找服务目录
安装路径：/opt/libreoffice6.1
快捷方式：/usr/bin/libreoffice6.1

启动服务
/usr/bin/libreoffice6.1 --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard




CentOS7安装字体库
在CentOS7服务器上，利用LibreOffice将word等格式转换为PDF，发现不支持汉字。需要安装字体库。

安装fontconfig
yum -y install fontconfig
安装完成后，/usr/share目录就可以看到fonts和fontconfig两个目录。

安装ttmkfdir
yum -y install ttmkfdir

检查已有字体库
fc-list

复制字体
#新建文件夹
mkdir /usr/share/fonts/chinese
把Windows系统的字体C:\Windows\Fonts复制进去。
simsun.ttc 宋体
simhei.ttf 黑体
msyh.ttf 微软雅黑
msyhbd.ttf 微软雅黑

# 修改字体权限
chmod -R 644 /usr/share/fonts/chinese

汇总生成fonts.scale文件
ttmkfdir -e /usr/share/X11/fonts/encodings/encodings.dir

修改字体配置文件
vim /etc/fonts/fonts.conf
修改内容
<fontconfig>
  ....
  <dir>....
  <dir>/usr/share/fonts/chinese</dir>
  ....
</fontconfig>

更新字体缓存
fc-cache -fv




