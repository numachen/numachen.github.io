---
date:
  created: 2024-09-19
draft: true
---

# Vue支持树形结构的组件

## 1. 背景
Vue项目中，需要展示树形结构的数据，并且需要支持筛选，搜索等功能，于是找到了[vue-treeselect](https://github.com/riophae/vue-treeselect)这个组件，这个组件功能很强大。

## 2. 资料连接
- 仓库：https://github.com/riophae/vue-treeselect
- 文档：https://vue-treeselect.js.org/

## 3. 项目使用
```html
npm install --save @riophae/vue-treeselect
```

## 4. 核心代码
```html
<template>
  <Card shadow>
    <Row type="flex" style="margin-bottom: 15px;">
      <Col span="10" style="float: left;">
        <h4>配置详情：<b style="font-size: 17px;">{{ this.$route.query['name'] }}</b></h4>
      </Col>
      <Col span="3" style="float: left;">
        <h4>动作：<b style="font-size: 17px;">{{ this.$route.query['action'] }}</b></h4>
      </Col>
      <Col span="1" offset="10">
        <Button type="primary" :loading="loading" @click="refresh" size="small">
          <span v-if="!loading">刷新</span>
          <span v-else>加载</span>
        </Button>
      </Col>
    </Row>
    <Row style="margin-bottom: 15px;">
      <Col span="6">
        <DatePicker type="datetimerange" placeholder="选择时间范围" style="width: 300px"
                    @on-change="getTime" :confirm="false"></DatePicker>
      </Col>
      <Col span="7">
        <treeselect v-model="relationValue"
                    placeholder="选择部门或者应用"
                    :show-count="true"
                    :options="relationsData" />
      </Col>
    </Row>

    <Table :loading="tableLoading" border :columns="detailColumns" :data="detailData"></Table>
  </Card>
</template>
<script>
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import { getHpaObj } from "@/api/devops-tools";
import { getDepartmentAndAppRelation } from "@/api/devops-tools";
export default {
  components: { Treeselect },
  data () {
    return {
      copiedData: null,
      relationsData: null,
      relationValue: '企迈公共SaaS',
      startTime: null,
      endTime: null,
      tableLoading: true,
      loading: false,
      detailColumns: [
        {
          title: '项目',
          key: 'project',
          minWidth: 160,
          maxWidth: 200
        },
        {
          title: '应用',
          key: 'app',
          width: 200,
        },
        {
          title: '部门',
          key: 'department',
          width: 200,
          render: (h, params) => {
            console.log(params.row._index, this.detailData)
            let tmp = this.relationsData[0]['children']
            let d = ''
            for (let i = 0; i < tmp.length; i++) {
              d = this.findDepartment(tmp[i], params.row.app)
              if (d) {
                this.detailData[params.row._index]['department'] = d['id']
                return h('span', d['id'])
              }
            }
          }
        },
        {
          title: '最小POD数',
          key: 'pod_min',
          width: 110,
          align: 'center',
          render: (h, params) => {
            let analysis = null
            let cpu = null
            if (params.row.analysis) {
              analysis = params.row.analysis
            }
            if (analysis) {
              cpu = analysis.hasOwnProperty('cpu_usage') ? analysis.cpu_usage : 0
            }
            // params.row.category !== 'k8s' ? '' : (cpu < 25 && params.row.pod_min > 5 ? '冗余' : '')
            return h('div', {
              style: {
                background: params.row.category !== 'k8s' ? '' : (cpu < 25 && params.row.pod_min > 5 ? '#5cadff' : '')
              }
            }, [h('Badge', {
              props: {
                // status:'warning',
                text: params.row.category !== 'k8s' ? '' : (cpu < 25 && params.row.pod_min > 5 ? '冗余' : ''),
                'class-name': 'demoBadge',
              },
              style: {
                fontSize: '10px !important;'
              }
            }, [h('span', params.row.pod_min)])])
          }
        },
        {
          title: '最大POD数',
          key: 'pod_max',
          width: 110,
          align: 'center'
        },
        {
          title: '总处理能力(最大值预估)',
          width: 160,
          render: (h, params) => {
            let analysis = null
            if (params.row.analysis) {
              analysis = params.row.analysis
            }
            let qps = null
            let tps = null
            let query_time = []
            let created_time = null
            let pods = null
            if (analysis) {
              qps = analysis.hasOwnProperty('qps') ? Math.ceil(analysis.qps) + '(qps/s)' : ''
              tps = analysis.hasOwnProperty('tps') ? Math.ceil(analysis.tps) + '(tps/s)' : ''
              query_time = analysis.hasOwnProperty('query_time_area') ? analysis.query_time_area : []
              created_time = analysis.hasOwnProperty('created_time') ? analysis.created_time : null
              pods = analysis.hasOwnProperty('pods') ? analysis.pods : null
            }
            return h('div', {
              class: 'textClass',
            }, [
              h('Tooltip', {
                props: {
                  placement: 'top',
                  content: '查询时间：' + query_time[0] + ' ~' + query_time[1] + '\n' +
                  '触发时间：' + created_time,
                  transfer: true,
                  maxWidth: 350,
                },
              },
              [h('span', {
                style: {whiteSpace: 'normal', wordBreak: 'break-all', fontWeight: 'bold', cursor: 'pointer'}
              }, [h('p', { style: {fontWeight: 'bold'}}, [
              h('span', qps),
              h('span', tps)
              ]), h('p', { style: {fontWeight: 'bold'}}, pods ? '当时POD数量：' + pods : '')])]
            )
            ]);
          }
        },
        {
          title: '单POD处理能力(最大值预估)',
          width: 120,
          render: (h, params) => {
            let analysis = null
            if (params.row.analysis) {
              analysis = params.row.analysis
            }
            let qps = null
            let tps = null
            if (analysis) {
              qps = analysis.hasOwnProperty('pod_qps') ? analysis.pod_qps + '(qps/s)' : ''
              tps = analysis.hasOwnProperty('pod_tps') ? analysis.pod_tps + '(tps/s)' : ''
            }
            return h('div', {
              class: 'textClass',
            },[h('span', {
                style: {whiteSpace: 'normal', wordBreak: 'break-all', fontWeight: 'bold', cursor: 'pointer'}
              }, [
              h('p', qps),
              h('p', tps)
              ])]);
          }
        },
        {
          title: 'CPU/MEM',
          key: 'level',
          width: 120,
          render: (h, params) => {
            let analysis = null
            if (params.row.analysis) {
              analysis = params.row.analysis
            }
            let cpu = ''
            let mem = ''
            if (analysis) {
              cpu = analysis.hasOwnProperty('cpu_usage') ? parseFloat(analysis.cpu_usage) : 0
              mem = analysis.hasOwnProperty('mem_usage') ? parseFloat(analysis.mem_usage).toFixed(2) + '%(mem)' : ''
            }
            return h('div', {
              class: 'textClass',
            }, [h('div', {
                style: {whiteSpace: 'normal', wordBreak: 'break-all', fontWeight: 'bold', cursor: 'pointer'}
              }, [
                h('p', { style: {fontWeight: 'bold', background: typeof cpu === 'number' && cpu < 25 ? '#5cadff' : ''}}, typeof cpu === 'number' ? cpu.toFixed(2) + '%(cpu)' : cpu),
                h('p', { style: {fontWeight: 'bold'}}, mem)])]);
          }
        },
        {
          title: '类别',
          key: 'category',
          width: 80,
          align: 'center'
        },
        {
          title: 'HPA名称',
          key: 'hpa_name',
          minWidth: 160,
        },
        {
          title: '集群名称',
          key: 'cluster',
          width: 110,
          align: 'center'
        },
        {
          title: '优先级',
          key: 'level',
          width: 110,
          align: 'center'
        },
      ],
      detailData: [],
      isInitialRelationValueChange: true, // 新增标志变量
    }
  },
  methods: {
    findDepartment(tree, targetApp) {
      // 递归查找部门
      if (typeof tree === 'object' && tree !== null) {
        if (tree.id === targetApp) {
          return tree;
        }
        for (let key in tree) {
          if (tree.hasOwnProperty(key)) {
            const result = this.findDepartment(tree[key], targetApp);
            if (result) {
              return tree;
            }
          }
        }
      } else if (Array.isArray(tree)) {
        for (let item of tree) {
          const result = this.findDepartment(item, targetApp);
          if (result) {
            return result;
          }
        }
      }
      return null;
    },
    getTime (s) {
      this.startTime = s[0]
      this.endTime = s[1]
      this.getHpaDetail()
    },
    refresh () {
      this.loading = true
      this.tableLoading = true
      this.getHpaDetail()
    },
    getHpaDetail () {
      this.tableLoading = true
      let data = {
        start_time: this.startTime,
        end_time: this.endTime,
      }
      getHpaObj(this.$route.query['id'], data).then(res => {
        if (res.status === 200) {
          this.loading = false
          this.tableLoading = false
          this.detailData = res.data.data[0]['configs']
        }
      })
    },
    getRelations () {
      getDepartmentAndAppRelation().then(res => {
        let r = res.data
        if (r.code !== 200) {
          return this.$Message.error(r.message)
        }
        this.relationsData = r.data
      })
    },
    filterDetailData(relationValue) {
      if (!relationValue || !this.detailData) {
        return;
      }
      this.detailData = this.copiedData.filter(item => {
        return (item.department && item.department.includes(relationValue))
      });
      if (this.detailData.length === 0) {
        this.detailData = this.copiedData.filter(item => {
          return (item.app && item.app.includes(relationValue))
        });
      }
    },
  },
  watch: {
    relationValue(newVal) {
      // 第一次初始化时，将数据拷贝到 copiedData 中
      if (this.isInitialRelationValueChange) {
        this.isInitialRelationValueChange = false; // 设置标志变量为 false
        this.copiedData = JSON.parse(JSON.stringify(this.detailData))
      }
      if (!newVal) {
        this.detailData = this.copiedData
      }
      this.filterDetailData(newVal);
    }
  },
  mounted () {
    this.getRelations()
    this.getHpaDetail()
  }
}
</script>
<style>
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
.demoBadge{
  font-size: 9px;
  top: -1px;
  position: relative;
  background-color: #ff9900;
}
</style>
```