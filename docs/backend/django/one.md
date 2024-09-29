---
date:
  created: 2024-09-25
draft: true
---

# Django 处理跨域

Django 处理跨域问题：No 'Access-Control-Allow-Origin' header is present on the requested resource
<!-- more -->

1. 安装django-cors-headers
```python
pip3 install django-cors-headers
```
2. 配置settings.py文件
```python
INSTALLED_APPS = [
    'corsheaders',
]
# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'Access-Control-Allow-Origin',
)
```


