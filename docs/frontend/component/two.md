---
date:
  created: 2024-09-29
draft: true
---

# 基于iView手撸一个Web页的API工具
## 1. 问题描述
测试需要一个网页版的API请求工具，方便测试人员自定义请求流程，方便对接自己的后端服务

## 2. 资料连接
代码地址：https://gitee.com/daoiskong/treasure-box/tree/master/view-ui-project

## 3. 核心代码
```html
<template>
<div>
  <Form ref="sceneFormData" :model="sceneFormData" :rules="ruleInline">
    <Card>
      <Row>
        <Col span="12">
          <h2>{{page || '创建请求链路'}}</h2>
        </Col>
        <Col span="6" offset="6">
            <a href="#"  @click="globalDrawer = true">全局参数</a> <Divider type="vertical" />
            <Button type="primary" @click="saveScene('sceneFormData')">保存</Button>
        </Col>
      </Row>
      <Row style="margin: 15px 0 15px 0">
        <Col span="4">
          <FormItem prop="name">
            <Input v-model="sceneFormData.name" placeholder="请输入场景名称" clearable />
          </FormItem>
        </Col>
        <Col span="19" style="display: inline-block" offset="1">
          <Row>
            <Col span="9">
              <FormItem prop="host">
                <Input v-model="sceneFormData.host" placeholder="请输入域名" clearable style="height: 10px;">
                  <Select v-model="sceneDomainPre" slot="prepend" style="width: 80px">
                    <Option value="http://">http://</Option>
                    <Option value="https://">https://</Option>
                  </Select>
                </Input>
              </FormItem>
            </Col>
          </Row>
        </Col>
      </Row>
      <RadioGroup v-model="sceneBtn" type="button" @on-change="switchGroup" size="large">
        <Radio label="场景配置"></Radio>
        <Radio label="施压配置"></Radio>
      </RadioGroup>
    </Card>

<!--创建链路-->
    <div style="margin-top: 15px;">
      <!--场景配置-->
      <Card v-if="isShow">
        <Button icon="md-add" @click="handleAddLink">新增串联链路</Button>

        <div style="margin-top: 15px;">
          <Card
            style="margin-top: 7px;"
            v-for="(item, index) in sceneFormData.tasksets"
            :key="index"
          >
            <Row>
              <Col span="5">
                <Icon type="ios-barcode-outline" size="25" style="margin-right: 7px;" />
                <span v-if="taskNameIsShow[index]" style="cursor: pointer;"
                      @click="showOrHide(index, taskNameIsShow)"
                >{{ item.taskset_name }}</span>
                <Input v-if="!taskNameIsShow[index]" v-model="item.taskset_name" placeholder="请输入链路名称" clearable
                       style="width: auto;"
                       @on-blur="showOrHide(index, taskNameIsShow)"
                />
              </Col>
              <Col span="1" offset="17">
                <Button type="text" size="small" style="color: red;" @click="handleRemoveLink(index)">删除链路</Button>
              </Col>
              <Col span="1" class="linkColClass" @click.native="showOrHide(index, arrowIsShow)" >
                <Icon v-if="arrowIsShow[index]" type="ios-arrow-down"  size="25" />
                <Icon v-if="!arrowIsShow[index]" type="ios-arrow-forward" size="25" />
              </Col>
            </Row>
            <div v-if="arrowIsShow[index]" style="margin-top: 15px;">
              <Card dis-hover
                    v-for="(api_item, api_index) in item.tasks"
                    :key="api_index"
                    style="margin-bottom: 15px;"
              >
                <div>
                  <Row>
                    <Col span="2" style="background-color: #00A0EE; width: 20px;text-align: center; margin-right: 10px;">{{api_index + 1}}</Col>
                    <Col :span="api_item.apiNameIsShow ? 2 : 4">
                      <b v-if="api_item.apiNameIsShow" style="line-height: 25px; cursor: pointer"
                         @click="linkShowOrHide(index, api_index, 'apiNameIsShow')">{{api_item.name}}</b>
                      <Input v-if="!api_item.apiNameIsShow" size="small" v-model="api_item.name"
                             placeholder="请输入接口名称" clearable style="width: auto;"
                             @on-blur="linkShowOrHide(index, api_index, 'apiNameIsShow')"
                      />
                    </Col>
                    <Col span="1" style="width: 80px;">
                      <Select v-model="api_item.method" size="small" @on-change="linkShowOrHide(index, api_index, 'methodSelectIsShow')">
                        <Option value="GET">GET</Option>
                        <Option value="POST">POST</Option>
                      </Select>
                    </Col>
                    <Col span="5">
                      <Input size="small" v-model="api_item.url" placeholder="请输入API路径" clearable />
                    </Col>
                    <Col span="1" offset="9">
                      <Button type="text" size="small" style="color: #2d8cf0;" @click="handleCopyLink(index, api_index)">复制API</Button>
                    </Col>
                    <Col span="1" align="center">
                      <Button type="text" size="small" style="color: red;" @click="handleRemoveAPI(index, api_index)">
                        <Icon type="ios-trash" size="20" />
                      </Button>
                    </Col>
                    <Col span="1" class="linkColClass" @click.native="linkShowOrHide(index, api_index, 'apiSelectIsShow')" >
                      <Icon v-if="api_item.apiSelectIsShow" type="ios-arrow-down"  size="25" />
                      <Icon v-if="!api_item.apiSelectIsShow" type="ios-arrow-forward" size="25" />
                    </Col>
                  </Row>

                  <Divider v-if="api_item.apiSelectIsShow" />

                  <Tabs v-if="api_item.apiSelectIsShow" value="name1" :animated="false" style="margin-top: -15px">
                    <TabPane label="请求头" name="name1">
                      <Row>
                        <Col span="3" style="margin-right: 15px;">参数名</Col>
                        <Col span="3" style="margin-right: 15px;">参数值</Col>
                        <Col span="3">操作</Col>
                      </Row>
                      <Row
                        style="margin-top: 7px;"
                        v-for="(header, h_index) in api_item.headers"
                        :key="h_index"
                      >
                        <Col span="3" style="margin-right: 15px;">
                          <Input size="small" v-model="header.label" placeholder="添加参数" clearable />
                        </Col>
                        <Col span="3" style="margin-right: 15px;">
                          <Input size="small" v-model="header.value" placeholder="参数值" clearable />
                        </Col>
                        <Col span="3">
                          <Icon type="ios-trash" size="20" style="color: #2d8cf0;cursor: pointer"
                                @click="handleRemoveHeader(index, api_index, h_index)" />
                        </Col>
                      </Row>
                      <Button size="small" style="margin-top: 15px;" @click="handleAddHeader(index, api_index)">添加</Button>
                    </TabPane>
                    <TabPane :label="api_item.method === 'POST' ? '请求体' : '请求参数'" name="name2">
                      <Row v-if="api_item.methodSelectIsShow" style="margin-bottom: 7px;">
                        <Col span="10">
                          <RadioGroup v-model="api_item.param_type" @on-change="linkShowOrHide(index, api_index, 'radioSwitchIsShow')">
                            <Radio label="raw"></Radio>
                            <Radio label="x-www-form-urlencoded"></Radio>
                          </RadioGroup>
                        </Col>
                      </Row>
                      <div v-if="!api_item.radioSwitchIsShow">
                        <Row>
                          <Col span="3" style="margin-right: 15px;">参数名</Col>
                          <Col span="3" style="margin-right: 15px;">参数值</Col>
                          <Col span="3">操作</Col>
                        </Row>
                        <Row
                          style="margin-top: 7px;"
                          v-for="(get_data, g_index) in api_item.get_data"
                          :key="g_index"
                        >
                          <Col span="3" style="margin-right: 15px;">
                            <Input size="small" v-model="get_data.label" placeholder="添加参数" clearable />
                          </Col>
                          <Col span="3" style="margin-right: 15px;">
                            <Input size="small" v-model="get_data.value" placeholder="参数值" clearable />
                          </Col>
                          <Col span="3">
                            <Icon type="ios-trash" size="20" style="color: #2d8cf0;cursor: pointer"
                                  @click="handleRemoveGetData(index, api_index, g_index)" />
                          </Col>
                        </Row>
                        <Button size="small" style="margin-top: 15px;" @click="handleAddGetData(index, api_index)">添加</Button>
                      </div>
                      <Row v-if="api_item.radioSwitchIsShow">
                        <Col span="12">
                          <Input v-model="api_item.post_data" type="textarea" :autosize="{minRows: 3,}" placeholder="请求参数" />
                        </Col>
                      </Row>
                    </TabPane>
                    <TabPane label="参数提取" name="name3">
                      <Row>
                        <Col span="3" style="margin-right: 15px;">参数名</Col>
                        <Col span="3" style="margin-right: 15px;">解析表达式</Col>
                        <Col span="1" style="margin-right: 15px;">随机匹配</Col>
                        <Col span="1">操作</Col>
                      </Row>
                      <Row
                        style="margin-top: 7px;"
                        v-for="(extract, e_index) in api_item.extracts"
                        :key="e_index"
                      >
                        <Col span="3" style="margin-right: 15px;">
                          <Input size="small" v-model="extract.key" placeholder="添加参数" clearable />
                        </Col>
                        <Col span="3" style="margin-right: 15px;">
                          <Input size="small" v-model="extract.expre" placeholder="参数值" clearable />
                        </Col>
                        <Col span="1" style="margin-right: 15px;">
                          <i-switch size="small"  v-model="extract.randomness"></i-switch>
                        </Col>
                        <Col span="1">
                          <Icon type="ios-trash" size="20" style="color: #2d8cf0;cursor: pointer"
                                @click="handleRemoveExtractData(index, api_index, e_index)" />
                        </Col>
                      </Row>
                      <Button size="small" style="margin-top: 15px;" @click="handleAddExtractData(index, api_index)">添加</Button>
                    </TabPane>
                    <TabPane label="断言" name="name4">
                      <RadioGroup v-model="api_item.assert_type">
                        <Radio :label="1">返回状态码为200</Radio>
                        <Radio :label="2">返回内容包含</Radio>
                        <Radio :label="3">返回内容不包含</Radio>
                        <Radio :label="4">正则匹配返回结果</Radio>
                        <Radio :label="5">正则不匹配返回结果</Radio>
                      </RadioGroup>
                      <Input v-model="api_item.key_word" type="textarea"
                             :disabled="api_item.assert_type === 1"
                             :autosize="{minRows: 3,}"
                             :placeholder="assert_type_obj_placeholder[api_item.assert_type]" />
                    </TabPane>
                    <TabPane label="配置" name="name5">
                      <Row>
                        <Col span="3">接口权重：<InputNumber size="small" v-model="api_item.task_weight" style="width: 60px;"
                                                      placeholder="请输入" clearable /></Col>
                      </Row>
                      <Row style="margin-top: 7px;">
                        <Col span="3">失败继续：<i-switch size="small" v-model="api_item.is_continue"></i-switch></Col>
                      </Row>
                    </TabPane>
                  </Tabs>
                </div>
              </Card>
              <Button icon="md-add" type="info" size="small" @click="handleAddAPI(index)">添加API</Button>
            </div>
          </Card>
        </div>
      </Card>

      <!--施压配置-->
      <Card v-if="!isShow">
        <div style="text-align:center">
          <Card dis-hover>
            <Table :columns="taskColumns" :data="taskData"></Table>
          </Card>
          <Card dis-hover style="margin-top: 15px;">
            <Row>
              <Col span="2">
                <b>压力机数量配置：</b>
              </Col>
              <Col span="3">
                <InputNumber v-model="sceneFormData.loadgens" placeholder="压力机数量配置" style="width: auto" />
              </Col>
            </Row>
            <Row style="margin-top: 10px;">
              <Col span="2">
                <b>接口等待时间：</b>
              </Col>
              <Col span="3">
                <InputNumber v-model="sceneFormData.wait_time" placeholder="接口等待时间" style="width: auto" />
              </Col>
            </Row>
          </Card>
        </div>
      </Card>
    </div>

<!--全局参数-->
    <Drawer title="全局参数"
            :closable="false"
            width="55%"
            v-model="globalDrawer">
      <Card dis-hover style="margin-bottom: 15px;">
        <Upload multiple
                accept="file"
                :before-upload="handleUpload"
                action="#">
          <Button icon="ios-cloud-upload-outline">选择文件</Button>
        </Upload>
        <Row v-for="(item, key) in customFile" :key="key">
          <Col span="10">
            <Alert size="small">{{item.name}}</Alert>
          </Col>
          <Col span="1" style="cursor: pointer" @click.native="removeFile(key)"><Icon size="30" type="ios-trash" /></Col>
        </Row>
      </Card>

      <Card dis-hover>
        <p slot="title">自定义参数</p>
        <Row
          style="margin-top: 7px;"
          v-for="(v, i) in sceneFormData.variables"
          :key="i"
          :gutter="6"
        >
          <Col span="6">
            <Input size="small" v-model="v.key" placeholder="添加参数" clearable style="width: auto;" >
              <span slot="prepend">参数名：</span>
            </Input>
          </Col>
          <Col span="5">
          <span class="inputPrefix">类型：</span>
            <Select size="small" v-model="v.variable_type" style="width: auto;" @on-change="switchOptionValue(v.variable_type, i)">
              <Option :value="1">固定值</Option>
              <Option :value="2">时间戳</Option>
              <Option :value="3">随机字符串</Option>
            </Select>
          </Col>
          <Col span="6" v-show="v.variable_type==1">
            <Input size="small" v-model="v.value" placeholder="常量值" clearable style="width: auto;" >
              <span slot="prepend">常量值：</span>
            </Input>
          </Col>
          <Col span="6" v-show="v.variable_type==2">
            <p style="display: inline-block;"> </p>
          </Col>
          <Col span="6" v-show="v.variable_type==3">
            <Input size="small" v-model="v.prefix" placeholder="常量值" clearable style="width: auto;" >
              <span slot="prepend">前缀：</span>
            </Input>
          </Col>
          <Col span="6" v-show="v.variable_type==3">
            <Input size="small" v-model="v.suffix" placeholder="常量值" clearable style="width: auto;" >
              <span slot="prepend">后缀：</span>
            </Input>
          </Col>
          <Col span="6" style="margin-top: 7px;" v-show="v.variable_type==3">
            <span class="inputPrefix">随机字符串个数：</span><InputNumber size="small" v-model="v.length" placeholder="常量值" clearable style="width: 75px;" />
          </Col>
          <Col span="6" style="margin-top: 7px;" v-show="v.variable_type==3">
            <Input size="small" v-model="v.ranges" placeholder="常量值" clearable style="width: auto;" >
              <span slot="prepend">随机字符串范围：</span>
            </Input>
          </Col>
          <Col span="1" :offset="v.variable_type==3 ? 11 : 6" :style="v.variable_type==3 ? 'margin-top: 7px' : ''">
            <Icon type="ios-trash" size="20" style="color: #2d8cf0;cursor: pointer"
                  @click="removeGlobalConfig(i)" />
          </Col>
        </Row>
        <Button size="small" style="margin-top: 15px;" @click="addGlobalConfig()">添加</Button>
      </Card>
    </Drawer>
  </Form>
</div>
</template>

<script>
// import {createScene, scenarioAction, taskExecUpdate} from '../api/performanceTesting'

export default {
  data () {
    return {
      page: '创建压测场景',
      taskId: 1,
      fileList: [],
      customFile: [],
      customDataType: 1,
      taskColumns: [
        {
          title: '串联链路',
          key: 'taskset_name'
        },
        {
          title: 'API数量',
          key: 'tasks',
          render: (h, params) => {
            return h('span', params.row.tasks.length)
          }
        },
        {
          title: '链路权重比',
          key: 'taskset_weight',
          render: (h, params) => {
            return h('InputNumber', {
              props: {
                value: params.row.taskset_weight
              },
              style: {
                width: "100px"
              },
              on: {
                input: (value) => {
                  this.sceneFormData.tasksets[params.row._index].taskset_weight = value
                }
              }
            })
          }
        }
      ],
      taskData: [],
      globalDrawer: false,
      requestMethod: 'GET',
      arrowIsShow: [true],
      taskNameIsShow: [true],
      isShow: true,
      sceneBtn: '场景配置',
      sceneDomainPre: 'http://',
      linkObjIndex: 1,
      apiObjIndex: 1,
      assert_type_obj_placeholder: {
        1: '判断返回状态码是否为200，并目返回内容不为空',
        2: '判断返回状态码是否为200，并且校验返回内容包含指定字符串',
        3: '判断返回状态码是否为200，并且校验返回内容不包含指定字符串',
        4: '判断返回状态码是否为200，并且校验返回内容能够通过正则表达式的匹配',
        5: '判断返回状态码是否为200，并且校验返回内容不能通过正则表达式的匹配',
      },
      sceneFormData: {
        name: '',
        host: '',
        tasksets: [
          {
            taskset_weight: 1,
            taskset_name: "串联链路1",
            tasks: [
              {
                name: "api_1",
                method: "GET",
                headers: [{label: 'content-type', value: 'application/json'}],
                url: "",
                assert_type: 1,
                key_word: "",
                is_continue: true,
                task_weight: 1,
                extracts:[],
                get_data: [{label: '', value: ''}],
                post_data: null,
                param_type: 'x-www-form-urlencoded',
                apiNameIsShow: true, // 标识是否开启编辑接口名称
                apiSelectIsShow: true,
                methodSelectIsShow: false,
                radioSwitchIsShow: false,
              }
            ]
          }
        ],
        variables: [],
        loadgens: 2,
        wait_time: 1
      },
      ruleInline: {
        name: [
          { required: true, message: '场景名称必填', trigger: 'blur' }
        ],
        host: [
          { required: true, message: '域名必填', trigger: 'blur' }
        ],
        taskset_name: [
          { required: true, message: '链路名称必填', trigger: 'blur' }
        ],
      }
    }
  },
  methods: {
    removeFile (i) {
      this.customFile.splice(i, 1)
    },
    handleUpload (file) {
      // 判断文件是否存在
      if (this.fileList.includes(file.name)) {
        return false
      }
      this.fileList.push(file.name)
      let index_1 = file.name.lastIndexOf('.')
      let index_2 = file.name.length
      let type_ = file.name.substring(index_1 + 1, index_2)
      if (type_ !== 'csv') {
        this.$Notice.warning({
          title: '文件格式不支持！',
          desc: '文件 ' + file.name + ' 格式不允许, 只允许csv格式！'
        })
        return false
      }
      this.customFile.push(file)
      return false
    },
    transferArrToDict (arr) {
      // 将数组转换为对象
      let obj = {};
      arr.forEach(item => {
        obj[item.label] = item.value;
      });
      return obj
    },
    transferDictToArr (obj) {
      let key = Object.keys(obj)[0]
      let value = obj[key]
      return [{"label": key, "value": value}]
    },
    switchOptionValue (e, i) {
      switch (e) {
        case 1:
          this.sceneFormData.variables.splice(i, 1)
          this.sceneFormData.variables[i] = {
            'variable_type': e,
            'key': '',
            'value': '',
          }
          break;
        case 2:
          this.sceneFormData.variables.splice(i, 1)
          this.sceneFormData.variables[i] = {
            'variable_type': e,
            'key': '',
          }
          break;
        case 3:
          this.sceneFormData.variables.splice(i, 1)
          this.sceneFormData.variables[i] = {
            'variable_type': e,
            'key': '',
            'prefix': '',
            'suffix': '',
            'ranges': '',
            'length': 1,
          }
          break;
      }
    },
    removeGlobalConfig (i) {
      this.sceneFormData.variables.splice(i,1)
    },
    addGlobalConfig () {
      this.sceneFormData.variables.push({
        'variable_type': 1,
        'key': '',
      })
    },
    // 复制API
    handleCopyLink (f_index, child_index) {
      this.sceneFormData.tasksets[f_index].tasks.push(this.sceneFormData.tasksets[f_index].tasks[child_index])
    },
    handleRemoveLink (i) {
      this.sceneFormData.tasksets.splice(i, 1)
    },
    handleRemoveAPI (f_index, child_index) {
      this.sceneFormData.tasksets[f_index].tasks.splice(child_index, 1)
    },
    linkShowOrHide (f_index, child_index, v) {
      this.sceneFormData.tasksets[f_index].tasks[child_index][v] = !this.sceneFormData.tasksets[f_index].tasks[child_index][v]
      if (this.sceneFormData.tasksets[f_index].tasks[child_index]['method'] === 'GET') {
        this.sceneFormData.tasksets[f_index].tasks[child_index]['param_type'] = 'x-www-form-urlencoded'
        this.sceneFormData.tasksets[f_index].tasks[child_index]['radioSwitchIsShow'] = false
      }
    },
    showOrHide (i, box) {
      box[i] = !box[i]
      box.push(false)
      box.pop()
    },
    handleAddAPI (f_index) {
      this.apiObjIndex++;
      this.sceneFormData.tasksets[f_index].tasks.push({
        name: "api_" + this.apiObjIndex,
        method: "GET",
        headers: [{label: 'content-type', value: 'application/json'}],
        url: "",
        assert_type: 1,
        key_word: "",
        is_continue: true,
        task_weight: 1,
        extracts:[{"key":"", "expre":"", "randomness": true}],
        get_data: [{label: '', value: ''}],
        post_data: null,
        param_type: 'x-www-form-urlencoded',
        apiNameIsShow: true, // 标识是否开启编辑接口名称
        apiSelectIsShow: true,
        methodSelectIsShow: false,
        radioSwitchIsShow: false,
      })
    },
    // 添加请求头参数
    handleAddHeader (f_index, child_index) {
      this.sceneFormData.tasksets[f_index].tasks[child_index].headers.push({
        label: '', value: ''
      })
    },
    // 删除请求头参数
    handleRemoveHeader (f_index, child_index, h_index) {
      this.sceneFormData.tasksets[f_index].tasks[child_index].headers.splice(h_index, 1)
    },
    // 添加get请求参数
    handleAddGetData (f_index, child_index) {
      this.sceneFormData.tasksets[f_index].tasks[child_index].get_data.push({
        label: '', value: ''
      })
    },
    // 删除get请求参数
    handleRemoveGetData (f_index, child_index, g_index) {
      this.sceneFormData.tasksets[f_index].tasks[child_index].get_data.splice(g_index, 1)
    },
    // 参数提取添加参数
    handleAddExtractData (f_index, child_index) {
      this.sceneFormData.tasksets[f_index].tasks[child_index].extracts.push({
        "key":"", "expre":"", "randomness": true
      })
    },
    // 参数提取删除参数
    handleRemoveExtractData (f_index, child_index, e_index) {
      this.sceneFormData.tasksets[f_index].tasks[child_index].extracts.splice(e_index, 1)
    },
    handleAddLink () {
      this.linkObjIndex++;
      this.arrowIsShow.push(false)
      this.taskNameIsShow.push(true)
      this.sceneFormData.tasksets.push(          {
        taskset_weight: 1,
        taskset_name: "串联链路" + this.linkObjIndex,
        tasks: [
          {
            name: "api_1",
            method: "GET",
            headers: [{label: 'content-type', value: 'application/json'}],
            url: "",
            assert_type: 1,
            key_word: "",
            is_continue: true,
            task_weight: 1,
            extracts:[{"key":"", "expre":"", "randomness": false}],
            get_data: [{label: '', value: ''}],
            post_data: null,
            param_type: 'x-www-form-urlencoded',
            apiNameIsShow: true, // 标识是否开启编辑接口名称
            apiSelectIsShow: true,
            methodSelectIsShow: false,
            radioSwitchIsShow: false,
          }
        ]
      })
    },
    switchGroup (t) {
      this.isShow = t !== '施压配置';
      this.taskData = this.sceneFormData.tasksets
    },
    saveScene (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          const task = this.sceneFormData.tasksets
          for (let i=0; i<task.length; i++) {
            if (!task[i]['taskset_name']) {
              this.$Message.error('链路名称必填!');
              return
            }
            if (!task[i]['taskset_weight']) {
              this.$Message.error('链路权重比必填!');
              return
            }
            const t_child = task[i]['tasks']
            // 处理前面自定义的数据类型，转换为接口需要的数据结构
            for (let ii=0; ii<t_child.length; ii++) {
              // 请求头
              t_child[ii]['headers'] = this.transferArrToDict(t_child[ii]['headers'])

              // 请求参数
              let json_data = {}
              if (t_child[ii]['method'] === 'POST' && t_child[ii]['param_type'] === 'raw') {
                json_data = t_child[ii]['post_data'] ? JSON.parse(t_child[ii]['post_data']) : null
              }
              if (t_child[ii]['method'] === 'POST' && t_child[ii]['param_type'] === 'x-www-form-urlencoded') {
                json_data = this.transferArrToDict(t_child[ii]['get_data'])
              }
              if (t_child[ii]['method'] === 'GET') {
                json_data = this.transferArrToDict(t_child[ii]['get_data'])
              }
              delete this.sceneFormData.tasksets[i].tasks[ii]['get_data']
              delete this.sceneFormData.tasksets[i].tasks[ii]['post_data']
              delete this.sceneFormData.tasksets[i].tasks[ii]['apiNameIsShow']
              delete this.sceneFormData.tasksets[i].tasks[ii]['apiSelectIsShow']
              delete this.sceneFormData.tasksets[i].tasks[ii]['methodSelectIsShow']
              delete this.sceneFormData.tasksets[i].tasks[ii]['radioSwitchIsShow']
              if (json_data) {t_child[ii]['json'] = json_data}
              if (t_child[ii]['method'] === 'GET' && json_data) {
                t_child[ii]['params'] = json_data
              }

              if (t_child[ii]['method'] === 'POST' && t_child[ii]['param_type'] === 'raw') {
                t_child[ii]['json'] = json_data
              } else {
                t_child[ii]['data'] = json_data
              }

              // 断言
              if (t_child[ii]['assert_type'] === 1) {
                delete this.sceneFormData.tasksets[i].tasks[ii]['key_word']
              }
              if (t_child[ii]['assert_type'] === 2 || t_child[ii]['assert_type'] === 3) {
                if (!t_child[ii]['key_word']) {
                  this.$Message.error('返回内容不能为空!');
                  return
                }
              }
              if (t_child[ii]['assert_type'] === 4 || t_child[ii]['assert_type'] === 5) {
                if (!t_child[ii]['key_word']) {
                  this.$Message.error('返回内容不能为空!');
                  return
                }
                t_child[ii]['pattern'] = t_child[ii]['key_word']
                delete this.sceneFormData.tasksets[i].tasks[ii]['key_word']
              }

              // 配置
              if (!t_child[ii]['task_weight']) {return this.$Message.error('接口权重不能为空!')}
            }
          }
          this.sceneFormData.host = this.sceneDomainPre + this.sceneFormData.host
          const formData = new FormData()
          formData.append('FILES', this.customFile)
          for (const f of this.customFile) {
            formData.append('FILES', f)
          }
          formData.append('data', JSON.stringify(this.sceneFormData))

          if (!this.taskId) {
            // createScene(formData).then(res => {
            //   let response = res.data
            //   if (response.code !== 200) {
            //     return this.$Message.error(res.message)
            //   }
            //
            //   this.sceneFormData = {
            //     name: '',
            //     host: '',
            //     tasksets: [
            //       {
            //         taskset_weight: 1,
            //         taskset_name: "串联链路1",
            //         tasks: [
            //           {
            //             name: "api_1",
            //             method: "GET",
            //             headers: [{label: 'content-type', value: 'application/json'}],
            //             url: "gw/org-center/account/login-v2/",
            //             assert_type: 1,
            //             key_word: "",
            //             is_continue: true,
            //             task_weight: 1,
            //             extracts:[{"key":"", "expre":"", "randomness": false}],
            //             get_data: [{label: '', value: ''}],
            //             post_data: null,
            //             param_type: 'x-www-form-urlencoded',
            //             apiNameIsShow: true, // 标识是否开启编辑接口名称
            //             apiSelectIsShow: true,
            //             methodSelectIsShow: false,
            //             radioSwitchIsShow: false,
            //           }
            //         ]
            //       }
            //     ],
            //     variables: [],
            //     loadgens: 2,
            //     wait_time: 1
            //   }
            //   this.$Message.success('场景创建成功!');
            //   setTimeout(() => {
            //     let route = this.$router.resolve({
            //       name: 'sceneList',
            //     })
            //     window.open(route.href, "_self")
            //   }, 2000)
            // })
          } else {
            // taskExecUpdate('POST', this.taskId, formData).then(res => {
            //   let response = res.data
            //   if (response.code !== 200) {
            //     return this.$Message.error(res.message)
            //   }
            //
            //   this.sceneFormData = {
            //     name: '',
            //     host: '',
            //     tasksets: [
            //       {
            //         taskset_weight: 1,
            //         taskset_name: "串联链路1",
            //         tasks: [
            //           {
            //             name: "api_1",
            //             method: "GET",
            //             headers: [{label: 'content-type', value: 'application/json'}],
            //             url: "",
            //             assert_type: 1,
            //             key_word: "",
            //             is_continue: true,
            //             task_weight: 1,
            //             extracts:[{"key":"", "expre":"", "randomness": false}],
            //             get_data: [{label: '', value: ''}],
            //             post_data: null,
            //             param_type: 'x-www-form-urlencoded',
            //             apiNameIsShow: true, // 标识是否开启编辑接口名称
            //             apiSelectIsShow: true,
            //             methodSelectIsShow: false,
            //             radioSwitchIsShow: false,
            //           }
            //         ]
            //       }
            //     ],
            //     variables: [],
            //     loadgens: 2,
            //     wait_time: 1
            //   }
            //   this.$Message.success('场景更新成功!');
            //   setTimeout(() => {
            //     let route = this.$router.resolve({
            //       name: 'sceneList',
            //     })
            //     window.open(route.href, "_self")
            //   }, 2000)
            // })
          }
        } else {
          this.$Message.error('请检查提交的参数!');
        }
      })
    },
    scenarioActionFunc () {
      this.sceneFormData = []
      // scenarioAction('GET', 'detail', this.taskId).then(res => {
      //   if (res.data.code !== 200) {
      //     this.$Message.error('获取详情报错！')
      //     return false
      //   }
      //   let data = res.data.data
      //   const task = data.tasksets
      //   for (let i=0; i<task.length; i++) {
      //     this.taskNameIsShow.push(true)
      //     const t_child = task[i]['tasks']
      //     // 处理前面自定义的数据类型，转换为接口需要的数据结构
      //     for (let ii=0; ii<t_child.length; ii++) {
      //       // 请求头
      //       t_child[ii]['headers'] = this.transferDictToArr(t_child[ii]['headers'])
      //
      //       data.tasksets[i].tasks[ii]['apiSelectIsShow'] = false
      //       data.tasksets[i].tasks[ii]['apiNameIsShow'] = false
      //
      //       data.tasksets[i].tasks[ii]['param_type'] = t_child[ii]['param_type']
      //
      //       if (t_child[ii]['method'] !== 'GET') {
      //         data.tasksets[i].tasks[ii]['methodSelectIsShow'] = true
      //       } else {
      //         data.tasksets[i].tasks[ii]['methodSelectIsShow'] = false
      //         data.tasksets[i].tasks[ii]['radioSwitchIsShow'] = false
      //         data.tasksets[i].tasks[ii]['get_data'] = this.transferDictToArr(t_child[ii]['json'])
      //       }
      //       if (t_child[ii]['method'] === 'POST' && t_child[ii]['param_type'] === 'raw') {
      //         data.tasksets[i].tasks[ii]['radioSwitchIsShow'] = true
      //         data.tasksets[i].tasks[ii]['get_data'] = []
      //         data.tasksets[i].tasks[ii]['post_data'] = t_child[ii]['json']
      //         t_child[ii]['post_data'] = JSON.stringify(t_child[ii]['json'])
      //       }
      //       if (t_child[ii]['method'] === 'POST' && t_child[ii]['param_type'] === 'x-www-form-urlencoded') {
      //         data.tasksets[i].tasks[ii]['radioSwitchIsShow'] = false
      //         data.tasksets[i].tasks[ii]['get_data'] = this.transferDictToArr(t_child[ii]['json'])
      //         data.tasksets[i].tasks[ii]['post_data'] = []
      //       }
      //
      //       // 断言
      //       if (t_child[ii]['assert_type'] === 1) {
      //         data.tasksets[i].tasks[ii]['key_word'] = ""
      //       }
      //       if (t_child[ii]['assert_type'] === 2 || t_child[ii]['assert_type'] === 3) {
      //         data.tasksets[i].tasks[ii]['key_word'] = ""
      //       }
      //       if (t_child[ii]['assert_type'] === 4 || t_child[ii]['assert_type'] === 5) {
      //         data.tasksets[i].tasks[ii]['key_word'] = t_child[ii]['pattern']
      //       }
      //
      //       // 配置
      //       if (!t_child[ii]['task_weight']) {return this.$Message.error('接口权重不能为空!')}
      //     }
      //   }
      //   let url = new URL(data.host);
      //   data.host = url.host
      //   this.sceneFormData = data
      // })
    }
  },
  mounted() {
    this.page = this.$route.query.page
    this.taskId = this.$route.query.id
    if (this.taskId) {this.scenarioActionFunc()}
  }
}
</script>

<style scoped>
.linkColClass {
  text-align: right;
}
.linkColClass:hover {
  color: #5cadff;
  cursor: pointer;
}
.inputPrefix {
  border: 1px solid #dcdee2;
  padding: 4px 0 5px 7px;
  background-color: #f8f8f9;
  font-size: 12px;
  border-right: none;
  border-radius: 4px 0 0 4px;
  margin-top: 3px;
}
</style>

```