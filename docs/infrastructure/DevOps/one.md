---
date:
  created: 2025-3-24
draft: true
---

# GitLab Runner 磁盘扩容与权限配置指南

<!-- more -->

## 问题背景
研发触发 GitLab CI/CD 流水线时出现以下问题：
1. 初始提示 `Node.js 环境缺失`
2. 安装环境后触发 `磁盘空间不足` 告警（原 `/opt` 目录挂载 20G 磁盘）
3. 添加 100G 新磁盘后因权限问题导致流水线构建异常

---

## 解决方案

### 一、磁盘扩容操作流程

#### 1. 查看当前磁盘信息
```bash
lsblk

NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
vda    253:0    0   20G  0 disk /
vdb    253:16   0  100G 0 disk /opt
```

#### 2. 格式化新磁盘（以 /dev/vdc 为例）
```bash
sudo mkfs.ext4 /dev/vdc
```

#### 3. 解除旧挂载
```bash
# 查看占用进程
lsof /opt
fuser -m -v /opt

# 强制卸载（若存在占用）
sudo umount -l /dev/vdb1 /opt
```

#### 4. 挂载新磁盘
```bash
sudo mount /dev/vdc /opt
```

#### 5. 配置永久挂载
```bash
echo '/dev/vdc /opt ext4 defaults 0 0' | sudo tee -a /etc/fstab
```

### 二、权限配置

#### 1. 创建目录并设置所有者
```bash
sudo mkdir -p /www/home
sudo chown -R www:www /opt
sudo chown -R www:www /www/home
```

#### 2. 重启 GitLab Runner
```bash
sudo systemctl restart gitlab-runner
sudo systemctl status gitlab-runner
```

### 三、SSH 密钥配置
#### 1. 生成部署密钥
```bash
ssh-keygen -t rsa -b 4096 -C "gitlab-runner@server"
cat /root/.ssh/id_rsa.pub
```

#### 2. 部署公钥到目标机
```bash
# 在目标服务器执行
mkdir -p /home/www/.ssh
echo "PUBLIC_KEY_CONTENT" >> /home/www/.ssh/authorized_keys
chmod 600 /home/www/.ssh/authorized_keys
```

### 四、CI/CD 部署配置

```bash
deploy_job:
  script:
    - webpath=/www/web/${CI_PROJECT_PATH_SLUG}/public_html
    - ssh www@192.168.192.69 "mkdir -p ${webpath}"
    - rsync --quiet -azv --delete ${buildSrc} www@192.168.192.69:${webpath}
```


## 关键注意事项

- **数据备份**
    - 挂载新磁盘前务必备份 `/opt` 目录数据
    - 推荐使用 `rsync -av /opt/ /tmp/opt_backup/`

- **权限继承**
     - 挂载后需重新设置目录权限：
     ```
     chmod 755 /opt
     chmod g+s /opt
     ```

- **服务依赖**
     - 重启 GitLab Runner 后验证服务状态：
     ```
     journalctl -u gitlab-runner -n 50 --no-pager
     ```

- **空间验证**
     ```
     df -h /opt | grep -v Filesystem | awk '{print "可用空间：" $4 "/" $2}'
     ```

------

## 故障排查记录

### 典型问题：构建成功但未同步文件

**原因分析**
`/www/home` 目录未正确设置所有者导致静默失败

**解决方案**
```
sudo chown -R www:www /www/home
find /www/home -type d -exec chmod 2775 {} \;
```

> 可通过 `CI_DEBUG_TRACE: "true"` 开启详细日志输出定位隐蔽问题
