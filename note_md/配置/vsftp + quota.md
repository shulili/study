### LVM分区
empty
### 配额
1. mkfs.ext4 /dev/ctvg/ctlv
2. mkdir /ftp
3. mount -o usrquota,grpquota /dev/ctvg/ctlv /ftp
4. quotacheck -augvc
5. quotaon -ugv /ftp
6. useradd -d /ftp/zhangsan zhangsan
7. passwd zhangsan
8. edquota zhangsan # 账号配额设置
9. rpm -ivh vsftpd-xxxx.rpm
10. systemctl start vsftpd
11. echo zhangsan > /etc/vsftpd/user_list
12. echo  -e 'anonymous\nftp' > /etc/vsftpd/user_list
13. echo userlist_deny=NO >> /etc/vsftpd/vsftpd.conf
14. systemctl restart vsftpd

## 虚拟用户
#### 安装
- rpm -ivh pam-1xxx.rpm
- rpm -ivh libdb-utils-5xxx.rpm
- rpm -ivh libdb-5xxxx.rpm

#### 验证信息文件
vim /etc/vsftpd/vusers.list
```
yujie
123456
andy
990990
```
- db_load -T -t hash -f /etc/vsftpd/vusers.list /etc/vsftpd/vusers.db
- chmod 600 /etc/vsftpd/vusers.*
- useradd -d /var/ftproot -s /sbin/nologin virtual
- chmod 755 /var/ftproot
vim /etc/pam.d/vsftpd.vu
```
#%PAM-1.0
auth    required    pam_userdb.so   db=/etc/vsftpd/vusers
account    required    pam_userdb.so   db=/etc/vsftpd/vusers
```
加入virtual、yujie、andy到/etc/vsftpd/user_list

- vim /etc/vsftpd/vsftp.conf
```
allow_writeable_chroot=YES
pam_service_name=vsftpd.vu
```
```
guest_enable=YES
guest_username=virtual
```
#### 独立授权配置
- vim /etc/vsftpd/vsftp.conf
```
user_config_dir=/etc/vsftpd/vusers_dir
```
vim ./yujie