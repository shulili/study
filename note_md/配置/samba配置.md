### 安装samba
### 建立samba用户
```
useradd zhangsan
pdbedit -a -u zhangsan
pdbedit -L #list all
pdbedit -vL zhangsan #list zhangsan详情
```
### 创建共享文件夹
最好设置其权限为777

### /ect/samba/smb.conf
```
[chaitin-share]
path=/share
public=yes
read only =yes
write list = admin
```
```
[xxx-home]
path=/manager
public=no
read only=yes
valid users = admin,@group_name
write list =admin

```
### 别名系统
```
vim /etc/samba/smbusers

root = admin supreme
zhangsan = zs

vim /etc/samba/smb.conf
[global]
username map = /etc/samba/smbusers
.....

service smb reload
```
### 访问地址限制
```
hosts allow = 192.168.4. 173.17.
hosts deny = 192.1.1.3
````

### smbclient
```
#查看
smbclient -L IPaddr
#登陆
smbclient //192.168.0.1/tmp  -U username%password
smbclient -L 198.168.0.1 -U username%password
```
#### systemctl restart nmb
#### systemctl restart smb
### windows
net use * /del
#删除所有登陆记录

\\192.168.100.1


