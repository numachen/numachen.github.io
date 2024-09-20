---
date:
  created: 2024-09-20
draft: true
---

# iview中的表格render搭配使用Tooltip 文字提示
## 1. 问题描述
- 在表格中加个Tooltip 文字提示，鼠标悬停显示全部内容

## 2. 资料连接
- https://v3.iviewui.com/components/tooltip

## 3. 核心代码
```html
{
  title: '总处理能力(最大值预估)',
  width: 120,
  align: 'center',
  render: (h, params) => {
    let analysis = null
    if (params.row.analysis) {
      analysis = params.row.analysis
    }
    let qps = analysis.qps ? analysis.qps + '(qps/s)' : ''
    let tps = analysis.tps ? analysis.tps + '(tps/s)' : ''
    return h('div', { 
      class: 'textClass',
    }, [
      h('Tooltip', {
        props: {
          placement: 'top',
          content: '查询时间：' + analysis.query_time_area[0] + ' ~' + analysis.query_time_area[1] + '\n' + 
          '触发时间：' + analysis.created_time,
          transfer: true,
          maxWidth: 200,
        },
      },
      [h('span', { 
        style: {whiteSpace: 'normal', wordBreak: 'break-all', fontWeight: 'bold', cursor: 'pointer'}
      }, [h('p', { style: {fontWeight: 'bold'}}, qps + tps), h('p', { style: {fontWeight: 'bold'}}, 'POD数量：' + analysis.pods)])]
    )
    ]);
  }
}

<style scoped>
.textClass {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  box-orient: vertical;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  max-height:42px
}
</style>
```