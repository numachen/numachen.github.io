---
date:
  created: 2024-12-11
draft: true
---

# Go高并发处理思路

### 详细解释
1. 定义任务：
- Score 结构体实现了 Job 接口的 Do 方法，Do 方法中处理任务并记录结果到全局变量 Box 中。
2. 工作池：
- WorkerPool 结构体管理多个 Worker，每个 Worker 从 JobQueue 中获取任务并执行。
- NewWorkerPool 函数创建一个新的工作池。
- Run 方法启动工作池，初始化多个 Worker 并启动它们。
3. 主函数：
- main 函数创建一个工作池，生成多个任务并将其放入 JobQueue。
- 使用 WaitGroup 等待所有任务完成。
- 打印结果并计算执行时间。

### 控制流图说明
- 开始：程序启动。
- 创建工作池：调用 NewWorkerPool 创建一个新的工作池。
- 启动工作池：调用 Run 方法启动工作池，初始化多个 Worker。
- 创建任务：生成多个任务并将其放入 JobQueue。
- 将任务放入JobQueue：将任务放入工作池的任务队列。
- 等待所有任务完成：使用 WaitGroup 等待所有任务完成。
- 打印结果：打印处理结果和执行时间。
- 结束：程序结束。

### 子图说明
- 工作池：
    - 初始化Worker：创建新的 Worker。
    - 启动Worker：启动每个 Worker。
    - 循环获取任务：从 JobQueue 中获取任务。
    - 分配任务给Worker：将任务分配给空闲的 Worker。
- Worker：
    - 从JobQueue获取任务：从 JobQueue 中获取任务。
    - 执行任务：调用任务的 Do 方法执行任务。
<!-- more -->

### 代码实现
```go
package main

// @project cncamp
// @description 高并发处理思路
// @author ChenWenMing
// @date 2024/11/27 14:53:56
// 博客：https://blog.csdn.net/weixin_42117918/article/details/107561920
// Go语言入门教程上：https://mp.weixin.qq.com/s/oAeHeyYr1Z7_yC8UsowE3w
// Go语言入门教程下：https://mp.weixin.qq.com/s/sA8VgNiO3omTAKvPWPwLYg

import (
	"fmt"
	"sync"
	"time"
)

// Score 定义一个实现Job接口的数据
type Score struct {
	Num int
	Wg  *sync.WaitGroup
	Box []int
}

var Box []int

// Do 定义对数据的处理
func (s *Score) Do() {
	defer s.Wg.Done()
	fmt.Println("num:", s.Num)
	// 处理接口放入全局变量中
	Box = append(Box, s.Num*7)
	time.Sleep(500 * time.Millisecond) //模拟执行的耗时任务
}

func main() {
	startTime := time.Now()
	//开启多少个线程
	num := 4
	// 注册工作池，传入任务
	// 参数1 worker并发个数
	p := NewWorkerPool(num)
	p.Run()
	var wg sync.WaitGroup
	// 处理多少条数据
	dataNum := 4
	for i := 1; i <= dataNum; i++ {
		wg.Add(1)
		go func(ii int) {
			sc := &Score{Num: ii, Wg: &wg}
			p.JobQueue <- sc //数据传进去会被自动执行Do()方法，具体对数据的处理自己在Do()方法中定义
		}(i)
	}

	wg.Wait()
	fmt.Println("main end", &Box)
	elapsedTime := time.Since(startTime)
	fmt.Printf("函数执行时间: %v\n", elapsedTime)

	//循环打印输出当前进程的Goroutine 个数
	//for {
	//	fmt.Println(*&p.JobQueue, 8888888888)
	//	fmt.Println("runtime.NumGoroutine() :", runtime.NumGoroutine())
	//	time.Sleep(5 * time.Second)
	//}
}

// Job --------------------------- Job ---------------------
type Job interface {
	Do()
}
type JobQueue chan Job

// Worker --------------------------- Worker ---------------------
type Worker struct {
	JobChan JobQueue //每一个worker对象具有JobQueue（队列）属性。
}

func NewWorker() Worker {
	return Worker{JobChan: make(chan Job)}
}

// Run 启动参与程序运行的Go程数量
func (w Worker) Run(wq chan JobQueue) {
	go func() {
		for {
			wq <- w.JobChan //处理任务的Go程队列数量有限，每运行1个，向队列中添加1个，队列剩余数量少1个 (JobChan入队列)
			select {
			case job := <-w.JobChan:
				fmt.Println("长度是", len(w.JobChan), "容量是", cap(w.JobChan))
				//fmt.Println("xxx2:",w.JobChan)
				job.Do() //执行操作
			}
		}
	}()
}

// WorkerPool --------------------------- WorkerPool ---------------------
type WorkerPool struct { //线程池：
	Workerlen   int           //线程池的大小
	JobQueue    JobQueue      //Job队列，接收外部的数据
	WorkerQueue chan JobQueue //worker队列：处理任务的Go程队列
}

func NewWorkerPool(workerlen int) *WorkerPool {
	return &WorkerPool{
		Workerlen:   workerlen,
		JobQueue:    make(JobQueue),
		WorkerQueue: make(chan JobQueue, workerlen),
	}
}
func (wp *WorkerPool) Run() {
	fmt.Println("初始化worker")
	//初始化worker(多个Go程)
	for i := 0; i < wp.Workerlen; i++ {
		worker := NewWorker()
		fmt.Println(i, "号worker启动")
		worker.Run(wp.WorkerQueue) //开启每一个Go程
	}
	// 循环获取可用的worker,往worker中写job
	go func() {
		for {
			select {
			//将JobQueue中的数据存入WorkerQueue
			case job := <-wp.JobQueue: //线程池中有需要待处理的任务(数据来自于请求的任务) :读取JobQueue中的内容
				fmt.Println("job:", job)
				worker := <-wp.WorkerQueue //队列中有空闲的Go程   ：读取WorkerQueue中的内容,类型为：JobQueue
				worker <- job              //空闲的Go程执行任务  ：整个job入队列（channel） 类型为：传递的参数（Score结构体）
				//fmt.Println("xxx1:", worker)
				//fmt.Printf("====%T  ;  %T======\n", job, worker)
			}
		}
	}()
}
```