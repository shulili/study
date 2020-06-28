#### 根据拓扑结构配置IPADDR、
#### 开启转发功能
```
vim /etc/squid.conf
+  http_port 192.168.3.1:3128 transparent
vim /etc/sysctl.conf
+  net.ipv4.ip_forward=1
sysctl -p
```
### 安装
1. 解压
2. `./configure  --prefix=/usr/local/squid --sysconfdir=/etc --enable-arp-acl  --enable-linux-netfilter  --enable-linux-tproxy  --enable-async-io=100  --enable-err-language="Simplify_Chinese"  --enable-nuderscore --enable-gnuregex`
3. make && make install
4. 添加系统用户

```
useradd -M -s /sbin/nologin squid
```

5. 改变属主属组权限

```
chown -R squid:squid /usr/local/squid/
chmod -R 755 /usr/local/squid/
# 如果出现logs权限问题
chmod -R 777 /usr/local/squid/var/logs
```

6. 杀死进程和重启服务

`killall -9 squid `
`/usr/local/squid/sbin/squid`

```
squid -k parse #检测配置文件语法
netstat -anpt | grep squid
```

7. 开启防火墙对流量进行转发
```
systemctl start firewalld
iptables -F
iptables -t nat -I PREROUTING -i ens33 -s 192.168.3.0/24 -p tcp --dport 80 -j REDIRECT --to-ports 3128
# 也可以额外加个其他端口443https
iptables -t nat -I PREROUTING -i ens33 -s 192.168.3.0/24 -p tcp --dport 443 -j REDIRECT --to-ports 3128
```
