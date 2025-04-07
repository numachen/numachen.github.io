---
date:
  created: 2025-3-24
draft: true
---

# Windows下使用软件连接解决C盘满的问题

#### 操作步骤

```bash
# 1. 使用SpaceSniffer软件分析C盘占用情况
# 2. 使用Windows中mklink命令创建软链接
mklink /d "C:\Users\chenwenming\AppData\Local\JetBrains\IntelliJIdea2023.3" "D:\AppData\Local\JetBrains\IntelliJIdea2023.3"
```
