---
date:
  created: 2024-10-16
draft: true
---

# Deepflow企业版部署流程

<!-- more -->

## ClickHouse安装、Mysql安装
#### 磁盘准备
```shell
# 1. 磁盘分区格式化
# 以fdisk为例，输入fdisk /dev/sdb进入分区界面。
# 输入n创建新分区，选择p创建主分区，按提示设置分区号和起始、结束位置（通常可以直接回车使用默认值）。
# 输入w保存并退出分区操作。
# 使用fdisk -l或lsblk命令检查分区是否成功。
# 2. 格式化分区
# 使用mkfs.ext4命令格式化分区，例如：mkfs.ext4 /dev/sdb1。
# 3. 挂载分区
# 创建挂载点目录，例如：mkdir /data
# 使用mount命令将分区挂载到挂载点，例如：mount /dev/sdb1 /data
# 4. 设置开机自动挂载
# 编辑/etc/fstab文件，添加以下内容：
# /dev/sdb1 /data ext4 defaults 0 0
# 使用mount -a命令重新挂载所有在/etc/fstab文件中配置的分区，以确保自动挂载设置生效
```
#### [ClickHouse安装](https://clickhouse.tech/docs/zh/getting-started/install/)
```text
# 安装步骤
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repo
sudo yum install -y clickhouse-server clickhouse-client

sudo /etc/init.d/clickhouse-server start
clickhouse-client # or "clickhouse-client --password" if you set up a password.


# 修改配置文件，允许远程登录
vim /etc/clickhouse-server/config.xml

<listen_host>0.0.0.0</listen_host>


# 创建账号，设置密码
CREATE USER new_user IDENTIFIED BY 'new_password';
GRANT ALL ON *.* TO new_user;
exit;

# 重启服务 
/etc/init.d/clickhouse-server restart

# 完成
```


#### [Mysql安装](https://dev.mysql.com/doc/refman/8.0/en/binary-installation.html)
```text
# 下载rpm包：https://dev.mysql.com/downloads/repo/yum/
# 安装流程
sudo dnf update -y
sudo dnf localinstall mysql80-community-release-el8-x.noarch.rpm
sudo dnf install mysql-community-server -y
sudo systemctl start mysqld
sudo systemctl enable mysqld
# 查看临时密码
sudo grep 'temporary password' /var/log/mysqld.log
mysql -u root -p
# 修改密码
ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
# 创建新用户
CREATE USER 'remote_user'@'%' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON *.* TO 'remote_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
# 客户端连接

# 完成
```