# APACHE
#### 卸载冲突软件
rpm -e httpd httpd-manual webalizer subversion mod_python mod_ssl mod_perl system-config-httpd php php-cli php-ldap php-common mysql dovecot --nodeps
#### 编译安装
tar  zxf  httpd-2.2.15.tar.gz  -C  /usr/src/

cd  /usr/src/httpd-2.2.15/

./configure --prefix=/usr/local/httpd --enable-so --enable-rewrite --enable-charset-lite --enable-cgi

make  &&  make  install
#### 优化执行路径
ln  -s  /usr/local/httpd/bin/*  /usr/local/bin/
#### 添加系统服务
cp  /usr/local/httpd/bin/apachectl  /etc/init.d/httpd

`service httpd restart`

vim  /etc/init.d/httpd
```
#!/bin/sh
#chkconfig:35 85 15
#description:apache
```
++35代表级别3和5，85 15代表开关++

chkconfig --add httpd
#### 修改主配置文件默认站点名称
vim  /usr/local/httpd/conf/httpd.conf

ServerName  www.chaitin.com
#### 开启服务
systemctl  start  httpd

netstat  -anpt  |  grep  80

# MYSQL
#### 确认系统没有rpm安装的mysql组件，如果有请卸载
rpm  -q  mysql-server  mysql
#### 开始安装mysql-5.5的编译环境，首先在光盘安装包目录安装==ncurses-devel==
rpm  -ivh  ncurses-devel-5.7-3.20090208.el6.x86_64.rpm
#### 然后安装==cmake==工具
tar  zxf   cmake-2.8.6.tar.gz

cd cmake-2.8.6

./configure

gmake && gmake install
#### 创建mysql所用的程序账户
useradd -u 49  -M  -s  /sbin/nologin  mysql
#### 解压缩mysql编译包
tar  zxf  mysql-5.5.22.tar.gz  -C  /usr/src

cd  /usr/src/mysql-5.5.22/
#### 配置mysql安装信息
```
cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DSYSCONFDIR=/etc -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DWITH_EXTRA_CHARSETS=all
```
#### 编译 && 编译安装mysql
make  &&  make  install
#### 修改mysql安装目录的归属
chown  -R  mysql:mysql  /usr/local/mysql
#### 根据实际情况复制配置文件样板，我们以中型数据库为例
cp  /usr/src/mysql-5.5.22/support-files/my-medium.cnf  /etc/my.cnf
#### 初始化数据库信息
/usr/local/mysql/scripts/mysql_install_db  --user=mysql  --basedir=/usr/local/mysql  --datadir=/usr/local/mysql/data
#### 优化命令执行路径
ln  -s  /usr/local/mysql/bin/*   /usr/local/bin/
#### 添加开机启动和系统服务
cp  /usr/src/mysql-5.5.22/support-files/mysql.server  /etc/init.d/mysqld

chmod  +x  /etc/init.d/mysqld

chkconfig  --add  mysqld

systemctl  start  mysqld
#### 登录mysql
mysql  -u  root 
```
# 为论坛准备数据库和管理员账户
CREATE  DATABASE  bbsdb;
#创建论坛数据库的管理人员
GRANT  all  ON  bbsdb.* TO  'bbsadmin'@'localhost'  IDENTIFIED  BY  '123.com';
# 退出数据库
quit
```
# PHP
#### 卸载相关软件
rpm -e php php-cli php-ldap php-common php-mysql --nodeps
#### 安装3个PHP需要的加密环境
```
tar zxf libmcrypt-2.5.8.tar.gz -C /usr/src/
cd /usr/src/libmcrypt-2.5.8/
./configure
make && make install
ln -s /usr/local/lib/libmcrypt.* /usr/lib/
```
```
tar zxf mhash-0.9.9.9.tar.gz -C /usr/src/
cd /usr/src/mhash-0.9.9.9/
./configure
make && make install
ln -s /usr/local/lib/libmhash* /usr/lib/
```
```
tar zxf mcrypt-2.6.8.tar.gz -C /usr/src/
cd /usr/src/mcrypt-2.6.8/
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
./configure
make && make install
```
#### 安装PHP环境
yum  -y  install  libxml2*
#### 安装PHP软件
```
tar zxf php-5.3.28.tar.gz -C /usr/src/
cd /usr/src/php-5.3.28/
./configure --prefix=/usr/local/php5  --with-mcrypt --with-apxs2=/usr/local/httpd/bin/apxs --with-mysql=/usr/local/mysql  --with-config-file-path=/usr/local/php5 --enable-mbstring
make && make install
```
#### 复制PHP主配置文件
```
cp /usr/src/php-5.3.28/php.ini-development /usr/local/php5/php.ini
```
#### 检查apache中是否被写入PHP信息
vim /usr/local/httpd/conf/httpd.conf
#### 配置文件中是否存在
LoadModule  php5_module        modules/libphp5.so
#### 在AddType出添加一行
AddType application/x-httpd-php .php
#### 添加php主页
DirectoryIndex  index.html  index.php
#### 重启httpd服务（如果php没加载，就重启两次）
systemctl  restart  httpd
#### 编写PHP测试页面
vim  /usr/local/httpd/htdocs/test1.php
```
<?php
phpinfo();
?>
```
##### 验证成功访问http://192.168.3.1/test1.php
#### 编写数据库测试文件
vim /usr/local/httpd/htdocs/test2.php
```
<?php
$link=mysql_connect('localhost','bbsadmin','123.com');
if($link) echo "gongxini，chengle！！";
mysql_close();
?>
```
##### 验证成功访问http://192.168.3.1/test2.php

### 安装论坛
#### 复制论坛的upload目录到网站根目录
cp  -r  /root/Discuz_7.2_FULL_SC_UTF8/upload/  /usr/local/httpd/htdocs/bbs
#### 修改论坛目录归属
```
cd /usr/local/httpd/htdocs/bbs/
chown -R daemon  templates/  attachments/  forumdata/ uc_client/data/cache/  config.inc.php
```
#### 访问论坛安装路径
- 改一下php.ini的short_open_tag
http://192.168.3.1/bbs/install 按照步骤进行论坛安装。对install目录执行移走，删除，去除权限等操作以防网站被初始化。