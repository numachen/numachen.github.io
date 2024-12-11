---
date:
  created: 2024-10-16
draft: true
---

# Centos7安装部署Sentry流程

#### 1、安装部署docker

```
sudo yum update
sudo yum instal l -y yum-utils device-mapper-persistent-data lvm2
sudo yum-conf ig- manager --add-repo https://download.docker.corn/linux/centos/docker-ce.repo
sudo yum update
sudo yum install -y docker-ce
# 启动docker
sudo systemctl start docker
```

#### 2、安装Python

1. 安装依赖环境　

```
# yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

 2.下载Python3
　　https://www.python.org/downloads/

```
# wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
```

3.安装python3

　　个人习惯安装在/usr/local/python3（具体安装位置看个人喜好）
　　创建目录：

```
# mkdir -p /usr/local/python3
```

解压下载好的Python-3.x.x.tgz包(具体包名因你下载的Python具体版本不不同⽽而不不同，如：我下载的是Python3.7.4.那我这里就是Python-3.7.4.tgz)

```
# tar -zxvf Python-3.7.4.tgz
```

4.进入解压后的目录，编译安装。

```
cd Python-3.7.4
./configure --prefix=/usr/local/python3
make && make install
```

5.建立python3的软链

```
# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
```

6.并将/usr/local/python3/bin加入PATH

```
# vim ~/.bash_profile
# .bash_profile
# Get the aliases and functions
if [ -f ~/.bashrc ]; then
. ~/.bashrc
fi
# User specific environment and startup programs
PATH=$PATH:$HOME/bin:/usr/local/python3/bin
export PATH
```

　　按ESC，输入:wq回车退出。

　　修改完记得执行行下面的命令，让上一步的修改生效：

```
# source ~/.bash_profile
```

　　检查Python3及pip3是否正常可用：

```
# python3 -V
Python 3.7.7
# pip3 -V
pip 20.1.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)

```

7.不行的话在创建一下pip3的软链接

```
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

#### 3、安装配置Sentry

1、上传解压onpremise-21.6.1.zip压缩包；

https://github.com/getsentry/onpremise/releases 安装的版本

```
# python安装docker-compose
pip install docker-compose
```

2、进入onpremise-21.6.1目录，执行命令

```
# 执行命令，查看缺失的相关配置，创建用户名、密码
./install.sh
# 执行启动命令
docker-compose up -d
```

3、浏览器登陆

localhost:9000



