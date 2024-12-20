---
date:
  created: 2024-12-20
draft: true
---

# Go工具库

### 背景
实用的代码片段

### 代码片段
```go
// 判断一个整数是否存在于切片中
func contains(slice []string, value string) bool {
	for _, v := range slice {
		if v == value {
			return true
		}
	}
	return false
}

// 判断一个子切片是否存在于父切片中
func containsPair(pairs []ClientServerPair, pair ClientServerPair) bool {
	for _, p := range pairs {
		if p.Client == pair.Client && p.Server == pair.Server {
			return true
		}
	}
	return false
}
```