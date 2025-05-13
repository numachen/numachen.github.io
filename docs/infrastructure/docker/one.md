---
date:
  created: 2025-5-13
draft: true
---

# Docker运行Nginx

<!-- more -->

### 问题背景
工作中使用到Nginx，原生的安装方式，繁琐且麻烦，还会遇到各种未知难解的问题，因此使用Docker。

---

### 安装及配置
```bash
######################
##   普通运行        ##
######################

# 创建文件夹，上传文件，启动容器
mkdir -p /etc/nginx/conf.d
mkdir -p /var/log/nginx

docker run -d --name nginx-server \
  -p 80:80 \
  -v /www:/www \
  -v /etc/nginx/conf.d:/etc/nginx/conf.d \
  -v /var/log/nginx:/var/log/nginx \
  registry.cn-shanghai.aliyuncs.com/numa-images/nginx:1.18.0



######################
## nginx配置证书     ##
######################

1. 存放证书目录
mkdir -p /etc/nginx/ssl


2. 启动命令
docker run -d --name nginx-server \
   -p 80:80 \
   -p 443:443 \
   -v /www:/www \
   -v /etc/nginx/conf.d:/etc/nginx/conf.d \
   -v /etc/nginx/nginx.conf:/etc/nginx/nginx.conf \
   -v /etc/nginx/ssl:/etc/nginx/ssl \
   -v /var/log/nginx:/var/log/nginx \
   registry.cn-shanghai.aliyuncs.com/numa-images/nginx:1.18.0

3. 配置文件
server {
    listen 80;
    listen 443 ssl;
    server_name your_domain.com;

    # SSL配置
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_prefer_server_ciphers on;
    
    # 网站根目录
    root /www;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}

4. 重启容器
docker restart nginx-server


######################
## 导出导入nginx镜像  ##
######################
docker save nginx:1.18.0 > nginx.tar
docker load -i nginx.tar
```
