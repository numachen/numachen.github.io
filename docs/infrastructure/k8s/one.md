---
date:
  created: 2024-02-21
draft: true
---

# Python通过API操作K8s集群

<!-- more -->

## 背景
在Python中使用Kubernetes API操作集群，可以方便地实现自动化部署、监控和管理Kubernetes集群中的资源。以下是一个简单的示例，演示如何使用Python的kubernetes-client库来操作Kubernetes集群。

## 安装kubernetes-client库
安装kubernetes-client库，可以使用pip工具进行安装。在Python环境中运行以下命令即可安装：
```shell
pip install kubernetes
```  

## 示例代码
以下是一个简单的示例代码，演示如何使用Python的kubernetes-client库来操作Kubernetes集群：
```python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
========================================
# @Author   : ChenWenMing
# @time     : 2025/02/21
# @File     : api_demo
# @Notes    : 
# @Description:
=========================================
"""

# k8sAPI接口文档：https://kubernetes.io/zh-cn/docs/tasks/administer-cluster/access-cluster-api/
# 示例：https://github.com/kubernetes-client/python/blob/master/examples/namespaced_custom_object.py

from kubernetes import client, config
from datetime import datetime, timedelta
import yaml

# 加载kubeconfig文件
config.load_kube_config(config_file=r"D:\qmai\code\backend\treasure-box\CloudNative\k8s_api\kube-config")


def get_overdue_services(api, days=15):
    """
    列出所有命名空间中运行超过15天的服务
    :param api: CoreV1Api 实例
    :param days: 超过多少天的服务
    """
    ret = api.list_service_for_all_namespaces(watch=False)
    for i in ret.items:
        creation_time = i.metadata.creation_timestamp
        if creation_time:
            age = datetime.now(creation_time.tzinfo) - creation_time
            if age > timedelta(days=days):
                print(f"Service: {i.metadata.name}, Namespace: {i.metadata.namespace}, Age: {age}")


apps_v1 = client.CoreV1Api()
get_overdue_services(apps_v1)


# 使用kubernetes包的功能更新目标服务deployment.yaml中的镜像版本
def update_image_version_in_deployment(api, namespace, deployment_name, new_version):
    """
    更新指定deployment的镜像版本
    :param api: AppsV1Api 实例
    :param namespace: 命名空间
    :param deployment_name: deployment名称
    :param new_version: 新的镜像版本
    """
    # 获取当前deployment的配置
    deployment = api.read_namespaced_deployment(name=deployment_name, namespace=namespace)

    # 更新容器镜像版本
    for container in deployment.spec.template.spec.containers:
        image_parts = container.image.split(':')
        if len(image_parts) == 2:
            container.image = f"{image_parts[0]}:{new_version}"
        else:
            container.image = f"{container.image}:{new_version}"

    # 更新deployment
    api.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)
    print(f"Image version in deployment {deployment_name} has been updated to {new_version}.")


# apps_v1 = client.AppsV1Api()
# update_image_version_in_deployment(apps_v1, "qmaiserver", "devopsassistant", "dev")


# 新增函数：通过更新服务配置来重启目标服务
def restart_service_by_update(c, namespace, service_name):
    """
    通过删除Pod实现重启逻辑：1.每次重启25%；2.对重启的Pod进行检查，是否Running；
    """
    try:
        # 获取当前服务的配置
        service = c.read_namespaced_service(name=service_name, namespace=namespace)
        print(service, 8989)

        # 获取与Service关联的Pod
        api_instance = client.CoreV1Api()
        label_selector = f"app={service_name.replace('-svc', '')}"  # 假设Service的标签为app=service_name
        pods = api_instance.list_namespaced_pod(namespace, label_selector=label_selector)

        total_pods = len(pods.items)
        remaining_pods = total_pods
        restart_count = max(1, int(total_pods * 0.25))  # 每次重启25%的Pod，至少重启1个Pod

        while remaining_pods > 0:
            # 随机选择需要重启的Pod
            import random
            pods_to_restart = random.sample(pods.items, min(restart_count, remaining_pods))

            # 删除选中的Pod以触发重启
            for pod in pods_to_restart:
                api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace=namespace)
                print(f"Pod {pod.metadata.name} has been deleted to trigger a restart.")

            print(
                f"Service {service_name} in namespace {namespace} has been restarted by deleting {len(pods_to_restart)} out of {total_pods} associated Pods.")

            # 等待Pod重新启动并变为Running状态
            import time
            for pod in pods_to_restart:
                while True:
                    new_pod = api_instance.read_namespaced_pod(name=pod.metadata.name, namespace=namespace)
                    if new_pod.status.phase == "Running":
                        print(f"Pod {pod.metadata.name} is now Running.")
                        time.sleep(1)
                        break
                    time.sleep(5)  # 每隔5秒检查一次Pod状态

            # 更新剩余Pod数量
            remaining_pods -= len(pods_to_restart)
            pods.items = [pod for pod in pods.items if
                          pod.metadata.name not in [p.metadata.name for p in pods_to_restart]]

        print(f"All Pods associated with service {service_name} in namespace {namespace} have been restarted.")
    except client.rest.ApiException as e:
        if e.status == 404:
            print(f"Service {service_name} not found in namespace {namespace}.")
        else:
            print(f"Failed to restart service {service_name}: {str(e)}")


# 在调用 restart_service_by_update 之前，先检查服务是否存在
# try:
#     v1.read_namespaced_service(name="devopsassistant-svc", namespace="qmaiserver")
#     restart_service_by_update(v1, "qmaiserver", "devopsassistant-svc")
# except client.rest.ApiException as e:
#     if e.status == 404:
#         print(f"Service devopsassistant not found in namespace qmaiserver.")
#     else:
#         print(f"Error checking service existence: {str(e)}")


# 新增函数：通过传参删除具体某个Pod
def delete_pod_by_name(api, namespace, pod_name):
    """
    通过Pod名称踢出具体的Pod
    :param api: kubernetes client
    :param namespace: 命名空间
    :param pod_name: Pod名称
    """
    try:
        api.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"Pod {pod_name} in namespace {namespace} has been deleted.")
    except client.rest.ApiException as e:
        if e.status == 404:
            print(f"Pod {pod_name} not found in namespace {namespace}.")
        else:
            print(f"Failed to delete pod {pod_name}: {str(e)}")

# api = client.CoreV1Api()
# delete_pod_by_name("qmaiserver", "devopsassistant-6985c594c6-pgj9p")

import datetime
import pytz


def restart_deployment(api, service_name, namespace):
    """
    通过更新部署模板的注释，触发服务重启
    :param api: kubernetes client
    :param service_name: 服务名称
    :param namespace: 命名空间
    """
    # 更新部署模板的注释，触发服务重启
    deployment = api.read_namespaced_deployment(name=service_name, namespace=namespace)
    deployment.spec.template.metadata.annotations = {
        "kubectl.kubernetes.io/restartedAt": datetime.datetime.now(tz=pytz.UTC)
        .isoformat()
    }

    # patch the deployment
    resp = api.patch_namespaced_deployment(
        name=service_name, namespace=namespace, body=deployment
    )

    print("\n[INFO] deployment `nginx-deployment` restarted.\n")
    print("%s\t\t\t%s\t%s" % ("NAME", "REVISION", "RESTARTED-AT"))
    print(
        "%s\t%s\t\t%s\n"
        % (
            resp.metadata.name,
            resp.metadata.generation,
            resp.spec.template.metadata.annotations,
        )
    )


apps_v1 = client.AppsV1Api()
restart_deployment(apps_v1, "devopsassistant", "qmaiserver")
```