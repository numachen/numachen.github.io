---
date:
  created: 2025-02-18
draft: true
---

# Flask多线程+缓存功能实现接口毫秒级响应

### 前言
最近有一个需求，需要实现有一个接口，获取CMDB里的服务和部门之间的关系，需要代码处理成一个树状结构，但是这个接口需要毫秒级响应，所以需要使用多线程+缓存功能实现接口毫秒级响应。
<!-- more -->

### 准备工作
`pip install Flask-Caching`

### 代码实现
```python
# 入口配置缓存
from flask_caching import Cache
import config

app = Flask(__name__)
api = Api(app, catch_all_404s=True)

cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
```
```python
# 业务代码
import json

from flask import request
from flask_restful import Resource
from concurrent.futures import ThreadPoolExecutor

from config.app import cache
from utils import response, get_ci, add_ci, update_ci, delete_ci


def fetch_department(item):
    bu = item['qmai_bu_name']
    department_data = {
        'id': bu,
        'label': bu,
        'children': [],
    }
    group_id = item['_id']
    group_payload = {
        'q': f"_type:70",
        'root_id': group_id,
        'count': 10000,
    }
    group_data = get_ci(group_payload, '/api/v0.1/ci_relations/s')
    tmp = []
    for item2 in group_data['result']:
        _id = item2['_id']
        group_name = item2['group_name']
        tem_dict = {
            'id': group_name,
            'label': group_name,
            'children': [],
        }
        app_param = {
            'q': f"_type:56",
            'root_id': _id,
            'count': 10000,
        }
        app_data = get_ci(app_param, '/api/v0.1/ci_relations/s')
        for item3 in app_data['result']:
            app_name = item3['app_name']
            tem_dict['children'].append({'id': app_name, 'label': app_name})
        tmp.append(tem_dict)
    department_data['children'].extend(tmp)
    return department_data


class GetDepartmentProRelation(Resource):
    """获取部门与项目的关系"""

    @cache.cached(timeout=7 * 24 * 3600)
    def get(self):
        bu_payload = {
            'q': f"_type:55",
            'root_id': 322,
            'use_id_filter': 1,
            'count': 10000,
        }
        # 1. 获得部门和应用的树形结构； 2. 根据应用获取对应部门
        # 一级部门：55，二级部门：70，获取应用：56
        map_data = get_ci(bu_payload, '/api/v0.1/ci_relations/s')
        department = {
            'id': '企迈公共SaaS',
            'label': '企迈公共SaaS',
            'children': [],
        }
        result = []

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(fetch_department, item) for item in map_data['result']]
            for future in futures:
                result.append(future.result())
        department['children'].extend(result)

        return response(data=department)

```