## 例子
- read -p "input：" IP
- ifconfig ens33 |grep inet | awk '{print $1" "$2}'|grep -v inet6 | awk -F. '{print $2}'
- id abc &> /dev/null && echo "abc user is exist" || useradd abc
- ==“free -m”表示以MB为单位==
- pgrep命令的“-x”表示查找时使用精确匹配
- let i++
- sed -i "s/^UUID/#&/g" testFile # &表示原来的东西
- 

#### sed
```
# -i 改文件
sed -i 's/^UUID/#&/g' testFile # &表示原来的东西
sed -i  '$a add somethings' testFile
sed -i '/^IP/ a newline' testFile
sed -i '/^123/d' testFile
sed -i '3,$d' testFile

```

## 正则表达式
- ^
- $
- \* ：匹配左侧表达式0到多次
- . : 一个任意字符
- \ : 使右侧正则符号失去含义
- [a-zA-Z] [a|b|c] : 范围选择匹配
`^[^0-9] : 不以数字开头的行`
`[[:lower:]]`
- {} : 匹配次数，需要转义为\\{\\}  `{3},{3,},{1,3}`

#### 拓展正则
- \+
- ？
- ｜
- （）
- （）+
## 运算
- expr A \\* B
- : +
- : -
- : \\*
- : /
- : %

## 判断
- test
- [  ]

==方括号“[”或“]”与条件表达式之间需要至少一个空格进行分隔==

#### 逻辑判断
- && : 逻辑与(and)
- || : 逻辑或(or)
- ! :  逻辑非
#### 文件判断
-e  -d  -f  -r  -w  -x
- -s : 套接字
- -c : 字符集设备
- -b : 块设备
#### 字符判断
=   !=  -z
#### 数值判断
-eq -ne -gt -lt -ge -le
## 条件
#### if
```
if [ -e  test ]
    then
    xxxxx
elif [ xxx ]
    then
    xxxxx
else
    xxxx
fi
```
#### case
```
case $X in
    "1")
    xxx
    ;;
    "2")

    ;;
    *)
    
    ;;
esac
```
## 循环
#### for
```
for i in X
do
done
```
#### while
```
while [  ]
do
done
```
## 特殊变量
- $RANDOW
- $# 命令行中位置变量的个数
- $* 所有位置变量的内容
- $? 上一条命令执行后返回的状态，当返回状态值为0时表示执行正常，非0值表示执行异常或出错
- $0 当前执行的进程/程序名

#### 环境变量
- `export Product`

## function
```
function demoFun1(){
    echo "这是我的第一个 shell 函数!"
    return `expr 1 + 1`
}
demoFun1
```
## 执行
- ./my.sh
- sh my.sh
- source my.sh

