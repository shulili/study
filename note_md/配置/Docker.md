# yum安装docker，打开docker
使用国内阿里云仓库
cr.console.aliyun.com
登录后在左下角找到镜像加速器，复制属于你自己的加速器地址例如：https://xxx.mirror.aliyuncs.com
然后在docker服务器修改/etc/docker/daemon.json
在{}里加入
`"registry-mirrors":["https://xxx.mirror.aliyuncs.com"]`
- docker search 镜像名  #搜索镜像
- docker pull docker.io/centos  #下拉镜像
- docker load -i 镜像包的位置
- docker images #查看本地镜像
#### 重启服务
- systemctl daemon-reload
- systemctl restart docker

### 启动镜像为容器或为容器开放端口
- docker run -itd [--name test1] 镜像名/镜像ID /bin/bash
- docker run -itd [--name test1] -p 真机端口:容器端口 镜像ID

### 查看/启动/停止容器
- docker ps（查看已运行） [-a]（查看所有）
- docker stop/start 容器ID/容器名字

### 进入容器
- docker exec -it 容器ID/容器名字 /bin/bash

### 启动容器时进行目录映射
- docker run -itd  -itd [--name test1] -p 真机端口:容器端口 -v 本机路径:容器路径 镜像ID 
- `docker run -itd --name nginx2 -p 802:80 -v /nginx-web/:/usr/share/nginx/html 9bee`
- docker cp 本地路径 容器ID:容器路径

### 创建自己的离线镜像
1. 找到基本镜像，开启为容器
2. 对容器内容进行修改，例如安装软件，修改配置，开启服务等
3. 将这个容器从新变为镜像

`docker commit 容器ID 镜像新名字:新tag标识`
4. 将这个镜像导出为tar包

`docker save -o 镜像保存位置和.tar文件名 镜像名称：tag标识`

#### 使用自检离线tar包回镜像
- docker load -i 镜像包的位置
#### 检查导入镜像
- docker images
- docker rmi——删除镜像
- docker rm——删除容器

# ==docker-群集swarm==
1. 配置IP地址，关闭selinx和防护墙，确保连通性
2. 设置ntp服务器同步时间戳
在node1上编辑/etc/ntp.conf
加入内容
```
server 127.127.1.0
fudge 127.127.1.0 stratum 8
```
---
所有客户机同步时间
`ntpdate 192.168.3.1`
---
3.在各个节点上修改主机名和hosts文件
vim /etc/hosts
```
192.168.3.1	node1
192.168.3.2	node2
192.168.3.3	node3
```
##### 临时改名
hostname node1
##### 永久改名（需要重启系统）
修改/etc/sysconfig/network
加入HOSTNAME=node1

###### 节点2和节点3也做同样配置
- ping node1
- ping node2
- ping node3
###### 都可以ping通即可

4. 设置node1可以密钥访问node2和node3
    1. node1上创建密钥兑
    `ssh-keygen回车回车回车`
    2. 将公钥传送到各节点
```
ssh-copy-id -i /root/.ssh/id_rsa.pub root@node1
ssh-copy-id -i /root/.ssh/id_rsa.pub root@node2
ssh-copy-id -i /root/.ssh/id_rsa.pub root@node3
```
###### node1可以免密码sshnode2和node3即可
```
ssh root@node2
ssh root @node3
ssh root@node3
```
5. 开始创建swarm群集领导者和节点
```
docker swarm init --advertise-addr 192.168.3.1
```
执行命令后会生成三行信息：
``` 
 docker swarm join \
    --token SWMTKN-1-3a4n4g9pekj0gz2p7wyoqc0jrcmeeks1bauxmx7emm3jl23fa4-buwmh6bc1f9c4u7aqjmprnas1 \
    192.168.3.1:2377
```
###### 在node2和node2上复制三行信息，并且执行，加入群集
---
#### 查看群集节点
docker node ls

---
6. 创建私有仓库
    1. 首先开启各个节点的转发功能并且关闭mtu，在node1上修改/etc/sysctl.conf
```
net.ipv4.ip_forward = 1
net.ipv4.ip_forward_use_pmtu = 0
```
    
执行调用`sysctl -p`

---
使用scp命令将sysctl.conf传送到node2和node3
```
scp /etc/sysctl.conf node2:/etc/
scp /etc/sysctl.conf node3:/etc/
```
---
在node2和node3上执行命令刷新
`sysctl -p`
---
拉取镜像registry:2或者使用tar包读取
`docker load -i /root/registry2.tar`
---
查看镜像导入正确
`docker images`
---
创建私有库存放目录
`mkdir -p /opt/data/registry`
---
开启私有库镜像到容器
`docker run -itd -p 5000:5000 --restart=always -v /opt/data/registry/:/var/lib/registry --name registry registry:2`
---
检查5000端口是否有私有库信息
`curl 192.168.3.1:5000/v2/_catalog`
---
修改docker的服务文件
`vim /usr/lib/systemd/system/docker.service`
---
在ExecStart=的最后一个选项后面输入
```
 \
--insecure-registry 192.168.3.1:5000
```
---             
保存退出重启daemon和docker
```
systemctl daemon-reload
systemctl restart docker
```
---
将服务文件复制到node2和node3并且全部重载daemon和重启docker服务
```
scp /usr/lib/systemd/system/docker.service  node2:/usr/lib/systemd/system/
scp /usr/lib/systemd/system/docker.service  node3:/usr/lib/systemd/system/
```
node2上
```
systemctl daemon-reload
systemctl restart docker
```
node3上
```
systemctl daemon-reload
systemctl restart docker
```

---
7. 在私有库上传镜像
    1. 使用pull或者载入的方式将nginx镜像导入
`docker load -i /root/nginx2.tar `
    2. 查看镜像是否导入成功
`docker images`
    3. 为nginx镜像设置另外一个内网tag方便识别
`docker tag nginx 192.168.3.1:5000/nginx`
    4. 查看是否成功
`docker images`
    5. 上传私有镜像到私有仓库
`docker push 192.168.3.1:5000/nginx`
    6. 查看私有仓库是否添加nginx
`curl 192.168.3.1:5000/v2/_catalog`
---
8. 创建swarm专用网络
`docker network create --driver overlay ct-network`
---
9. 安装swarm的图形化见识工具
导入镜像
`docker load -i /root/visualizer.tar`
---
发布到私有库

`docker tag dockersamples/visualizer 192.168.3.1:5000/visualizer`

`docker push 192.168.3.1:5000/visualizer`

---
##### 开启容器查看8888端口是否出现管理器界面
`docker run -itd -p 8888:8080 -e HOST=192.168.3.1 -e PORT=8080 -v /var/run/docker.sock:/var/run/docker.sock --name visualizer 192.168.3.1:5000/visualizer`
##### 浏览器访问http://192.168.3.1:8888
---
10. 在群集中开启nginx镜像，看到个节点启动情况

`docker service  create --replicas 4 --network ct-network --name web -p 80:80 192.168.3.1:5000/nginx`

查看群集信息
```
docker service ps web
docker service ls
```
11. 验证，单个修改容器内的网页信息，强制刷新页面看到群集节点切换访问。关闭某个节点服务器，会看到容器被开到了其他节点，保持总容器数量。
12. 调整群集内节点数量
`docker service scale web=13`


13.关闭web群集，新建一个挂载真机目录的群集（每个节点都必须存在相同路径的目录）
```
docker service  rm web
mkdir /nginxweb
docker service create --replicas 8 --network ct-network --name web1 -p 80:80 --mount type=bind,src=/nginxweb/,dst=/usr/share/nginx/html/ 192.168.3.1:5000/nginx
```