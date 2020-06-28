### 本地yum
1. 删除原有repo
2. 创建自己的yum
```
[local-yum]
name=local-yum
baseurl=file:///media/
enabled=1
gpgcheck=0
```