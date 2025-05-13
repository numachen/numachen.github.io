---
date:
  created: 2025-5-13
draft: true
---

# Docker运行Redis、Mysql

<!-- more -->

### 一、 安装Docker
(1) 安装Docker
```bash
sudo apt-get update
apt install docker.io
```

(2) 配置镜像加速器
```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://4fjpr3fg.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```


### 二、Redis5.0安装
(1) 创建本地数据目录：
确保本地的/data/redis/目录存在并且Docker有权限访问它。
```bash
mkdir -p /data/redis
```

(2) 拉取Redis镜像：
```bash
docker pull redis:5.0
```

(3) 运行Redis容器并挂载数据目录：
使用docker run命令启动Redis容器，并将本地的/data/redis/目录挂载到容器内的/data目录。
```bash
docker run -d --name redis-container -v /data/redis:/data -p 6379:6379 --restart always redis:5.0
```
   解释：<br>
  -d：以分离模式（后台）运行容器。 <br>
  --name redis-container：为容器指定一个名称。 <br>
  -v /data/redis:/data：将本地的/data/redis/目录挂载到容器内的/data目录。 <br>
  redis:5.0：指定要使用的Redis镜像版本。 <br>
  redis-server --appendonly yes：启动Redis服务器并启用AOF持久化。 <br>

(4) 连接到Redis容器：
如果需要连接到Redis容器进行测试，可以使用以下命令：
```bash
docker exec -it redis-container redis-cli
# 测试Redis是否正常,返回PONG说明运行正常
ping
```

### 三、Mysql8.0安装
安装过程
```bash
# 创建本地数据和配置目录
sudo mkdir -p /data/mysql
sudo chown -R $USER:$USER /data/mysql

# 拉取MySQL 8.0镜像
docker pull mysql:8.0

# 运行MySQL容器并挂载数据和配置目录
docker run -d \
  --name mysql-container \
  -v /data/mysql:/var/lib/mysql \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=qmai2025\
  --restart always \
  mysql:8.0

# 验证MySQL容器是否运行
docker ps

# 连接到MySQL容器
docker exec -it mysql-container mysql -uroot -p

# 更改用户认证插件
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'qmai2025';
FLUSH PRIVILEGES;


#####################
# 进入容器开启gitd
# 开启gitd
-- 开启GTID一致性模式
SET @@GLOBAL.ENFORCE_GTID_CONSISTENCY = ON;

-- 第1步：设置GTID_MODE为OFF_PERMISSIVE
SET @@GLOBAL.GTID_MODE = OFF_PERMISSIVE;

-- 第2步：设置GTID_MODE为ON_PERMISSIVE
SET @@GLOBAL.GTID_MODE = ON_PERMISSIVE;

-- 第3步：最后设置GTID_MODE为ON
SET @@GLOBAL.GTID_MODE = ON;

# 验证
-- 检查GTID模式
SHOW VARIABLES LIKE 'gtid_mode';

-- 检查GTID一致性设置
SHOW VARIABLES LIKE 'enforce_gtid_consistency';

```