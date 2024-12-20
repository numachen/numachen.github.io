---
date:
  created: 2024-12-19
draft: true
---

# 携程&管道的一次实践

### 背景
为了提升接口查询速度，将循环查询数据库的操作，使用go并发实现，基于goroutine&channel实现

### 代码实现
```go
func getAppMetrics(l *TraceMapLogic, req *types.TopoNewReq, res [][]interface{}) (resp map[string]interface{}, err error) {
	host := l.svcCtx.Config.MonitorDB.Host
	user := l.svcCtx.Config.MonitorDB.User
	pass := l.svcCtx.Config.MonitorDB.Password
	dsn := fmt.Sprintf("%s:%s@tcp(%s:3306)/monitor_report?charset=utf8mb4&parseTime=True&loc=Local", user, pass, host)
	conn := sqlx.NewMysql(dsn)
	result := &types.QueryServerMetric{}
	var server = make(map[string]interface{})

	var c []*types.ServerMetrics
	var wg sync.WaitGroup
	// 创建一个通道来接收子节点数据
	childChan := make(chan *types.ServerMetrics, len(res))
	errChan := make(chan error, len(res))
	for _, value := range res {
		wg.Add(1)
		go func(val []interface{}) {
			defer wg.Done()
			query := "SELECT pods, cpu_usage, mem_usage, qps FROM monitor_report_statistics.monitor_statistics WHERE app_name = ? ORDER BY id DESC"
			err := conn.QueryRowCtx(context.Background(), result, query, val[0])
			// 检查是否有数据
			if err != nil {
				errChan <- err
				return
			}
			var child = &types.ServerMetrics{
				Name:    val[0].(string),
				Value:   val[0].(string),
				ID:      uuid.New().String(),
				Warning: nil,
			}
			child.Metrics.Pods = result.Pods
			child.Metrics.CpuUsage = math.Round(result.CpuUsage*10) / 10
			child.Metrics.MemUsage = math.Round(result.MemUsage*10) / 10
			child.Metrics.Qps = math.Round(result.Qps*10) / 10
			childChan <- child
			fmt.Println("Goroutine completed for:", child)
		}(value)
	}
	go func() {
		wg.Wait()
		close(childChan)
		close(errChan)
	}()

	// 使用无限循环读取通道数据
	for {
		select {
		case child, ok := <-childChan:
			if !ok {
				goto done
			}
			c = append(c, child)
		case err := <-errChan:
			if err != nil {
				return nil, err
			}
		}
	}
done:
	server["children"] = c
	return server, nil
}
```