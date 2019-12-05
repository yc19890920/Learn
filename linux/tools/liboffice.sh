#!/bin/bash
#author:luzi
#此脚本运行环境需要JAVA，依托liboffice实现预览，安装前会进行JAVA环境检查，没有会进行安装，然后会拷贝windows字体包至系统并刷新字体缓存
# 检测 yum 程序
check_yum_program()
{
    [ -e /usr/bin/yum ] && return 0
    echo "Error: Can't found yum command!"
    exit 2
}

######################Step1:Install Dependence#######################
echo "Step1:Check and Install JAVA"
check_yum_program
yum install wget screen epel-release -y
if [ $? -ne 0 ]; then
                echo "Yum Failed.Pls Check Network.Exit"
		exit 1
        fi

######################Step2:Check and Install JAVA#######################
echo "Step2:Check and Install JAVA"
java -version
if [ $? -ne 0 ]; then
    echo "No JAVA.Begin install JAVA..."
    wget --no-check-certificate http://download.comingchina.com/temp/jdk-8u201-linux-x64.tar.gz
    mkdir /usr/java
    tar -zxvf jdk-8u201-linux-x64.tar.gz -C /usr/java/ >/dev/null 2>&1
    echo '##############JAVA###################' >>/etc/profile
    echo 'JAVA_HOME=/usr/java/jdk1.8.0_201' >>/etc/profile
    echo 'CLASSPATH=$JAVA_HOME/lib/' >>/etc/profile
    echo 'PATH=$PATH:$JAVA_HOME/bin' >>/etc/profile
    echo 'export PATH JAVA_HOME CLASSPATH' >>/etc/profile
    source /etc/profile
    java -version
	if [ $? -ne 0 ]; then
	    	echo "JAVA Install Fail.Exit"
		exit 1
	else
    		echo "JAVA Install Success.Dir is /usr/java/"
			rm jdk-8u201-linux-x64.tar.gz -fv
	fi
else
    echo "JAVA has been installed."
fi

######################Step3:Install LibeOffice#######################
echo "Step3:Install LibeOffice"
wget -N -P /tmp/office http://download.comingchina.com/temp/LibreOffice_6.1.5_Linux_x86-64_rpm.tar.gz
wget -N -P /tmp/office http://download.comingchina.com/temp/LibreOffice_6.1.5_Linux_x86-64_rpm_langpack_zh-CN.tar.gz
tar zxvf /tmp/office/LibreOffice_6.1.5_Linux_x86-64_rpm.tar.gz -C /tmp/office >/dev/null 2>&1
tar zxvf /tmp/office/LibreOffice_6.1.5_Linux_x86-64_rpm_langpack_zh-CN.tar.gz -C /tmp/office >/dev/null 2>&1

yum install /tmp/office/LibreOffice_6.1.5.2_Linux_x86-64_rpm/RPMS/*.rpm -y
yum install /tmp/office/LibreOffice_6.1.5.2_Linux_x86-64_rpm_langpack_zh-CN/RPMS/*.rpm -y

######################Step4:Copy Windows Fonts#######################
echo "Step4:Copy Windows Fonts"
yum install ibus -y
yum -y install fontconfig
yum -y install ttmkfdir
mkdir /usr/share/fonts/chinese
wget -N -P /root/ http://download.comingchina.com/temp/yulan.zip
unzip /root/yulan.zip >/dev/null 2>&1
cp /root/yulan/* /usr/share/fonts/chinese
chmod -R 644 /usr/share/fonts/chinese
ttmkfdir -e /usr/share/X11/fonts/encodings/encodings.dir
sed -i  '/<dir>\/usr\/share\/fonts<\/dir>/a\        <dir>\/usr\/share\/fonts\/chinese<\/dir>' /etc/fonts/fonts.conf
fc-cache -fv


######################Step5:Start in the background#######################
echo "Step5:Start in the background"
/usr/bin/libreoffice6.1 --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard &
netstat -tpln|grep 8100
sleep 2
if [ $? -ne 0 ]; then
         echo "Start Failed"
    else
         echo "Start Success.Complete"
fi



