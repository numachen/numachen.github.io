---
date:
  created: 2024-09-19
draft: true
---

# Vue数据加载瀑布流

## 1. 背景
Vue项目中，加载数据需要支持瀑布流和分页两种方式，原来支持了分页，现在需要支持瀑布流。本来是很简单的一个问题，却用了三天的时间。
问题出在一直无法获取滚动条滚动的高度，也是自己陷入了思维定式。因为这个页面是嵌套在home页中，我在子页面中无法监听到父组件的滚动事件。
最后，通过全局状态管理器vuex，解决了这个问题。父组件增加handleScroll方法，将鼠标滚动高度传递给vuex，然后通过vuex获取滚动条滚动高度。

## 2. 核心代码
父组件通过方法将数据存储到vuex中：
```Vue
<template>
  <div id="home" :class="{
    home: !isCollapse,
    'home-close': isCollapse,
    'home-iframe': isIframe
  }" @scroll.passive="handleScroll"
  >
    <div class="home-top">
      <template v-if="!isIframe">
        <i v-if="!isCollapse " class="el-icon-s-fold" @click="updateCollapse"></i>
        <i v-else class="el-icon-s-unfold" @click="updateCollapse"></i>
      </template>

      <div class="header-right">
        <el-dropdown class="el-dropdown-box" split-button>
          <!-- <el-button type="primary"></el-button> -->
          {{ areaLabel }}
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="item in $store.state.areaList" :key="item.value">
              <div class="drop-item" @click="selectArea(item.value)">{{ item.label }}</div>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <el-dropdown class="el-dropdown-box"  v-if="!isIframe">
          <span class="el-dropdown-link">
            <el-avatar :size="size" :src="circleUrl"></el-avatar>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>
              <div class="drop-item">你好-{{ userName }}</div>
            </el-dropdown-item>
            <el-dropdown-item>
              <div class="drop-item" @click="logout">退出登录</div>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <div class="contain" :style="paddingLeftStyle">
      <router-view />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { getAppConfig } from './../http/config'
const appConfig = getAppConfig()
export default {
  name: 'Home',
  data() {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      size: 'large',
      userName: '',
      scrollDebounce: null
    }
  },
  computed: {
    isCollapse() {
      return this.$store.state.isCollapse
    },
    areaLabel() {
      return this.$store.state.areaList.find(item => item.value === this.$store.state.area).label
    },
    paddingLeftStyle() {
      const { path } = this.$route
      let paddingLeft = '20px'
      if (path.includes('/alicloudLog')) {
        paddingLeft = '0'
      } else if (path.includes('/SkyWalking')) {
        paddingLeft = '10px'
      }
      return {
        paddingLeft
      }
    }
  },
  beforeDestroy() {
    const homeDiv = document.getElementById('home')
    if (homeDiv) {
      homeDiv.removeEventListener('scroll', this.handleScroll)
    }
  },
  methods: {
    handleScroll(event) {
      clearTimeout(this.scrollDebounce)
      this.scrollDebounce = setTimeout(() => {
        const scrollTop = event.target.scrollTop
        const containerHeight = event.target.clientHeight
        const scrollHeight = event.target.scrollHeight
        this.$store.commit('updateScrollTop', scrollTop)
        this.$store.commit('updateClientHeight', containerHeight)
        this.$store.commit('updateScrollHeight', scrollHeight)
        const distanceToBottom = scrollHeight - (scrollTop + containerHeight)
        if (this.$store.state.pageDataNum >= this.$store.state.pageTotal) {
          return
        }
        if (distanceToBottom <= 50 && this.$store.state.pagingType && !this.$store.state.isBtnOrScrollClick) {
          event.target.scrollTop = event.target.scrollTop - 80
        }
      }, 100) // 100ms防抖时间
    },
    getCookies(key) {
      var search = key + '='
      var returnvalue = ''
      if (document.cookie.length > 0) {
        var offset = document.cookie.indexOf(search)
        if (offset !== -1) {
          offset += search.length // 已经存在cookies内
          var end = document.cookie.indexOf(';', offset) // set index of beginning of value
          if (end === -1) { end = document.cookie.length }
          returnvalue = unescape(document.cookie.substring(offset, end))
        }
      }
      return returnvalue
    },
    // 切换区域
    selectArea(val) {
      localStorage.setItem('area', val)
      const { removeQueryList } = this.$store.state
      let query = { area: val }
      const isRemove = removeQueryList.includes(this.$route.path)
      if (!isRemove) {
        query = { ...this.$route.query, ...query }
      }
      this.$router.push({ ...this.$route, query })
      this.$router.go(0)
    },
    baseDecode(e) {
      const _keyStr =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
      var t = ''
      var n, r, i
      var s, o, u, a
      var f = 0
      e = e.replace(/[^A-Za-z0-9+/=]/g, '')
      while (f < e.length) {
        s = _keyStr.indexOf(e.charAt(f++))
        o = _keyStr.indexOf(e.charAt(f++))
        u = _keyStr.indexOf(e.charAt(f++))
        a = _keyStr.indexOf(e.charAt(f++))
        n = (s << 2) | (o >> 4)
        r = ((o & 15) << 4) | (u >> 2)
        i = ((u & 3) << 6) | a
        t = t + String.fromCharCode(n)
        if (u !== 64) {
          t = t + String.fromCharCode(r)
        }
        if (a !== 64) {
          t = t + String.fromCharCode(i)
        }
      }
      t = this._utf8_decode(t)
      return t
    },

    _utf8_decode(e) {
      var t = ''
      var n = 0
      // eslint-disable-next-line no-undef
      var r = 0
      var c2 = 0
      var c3
      while (n < e.length) {
        r = e.charCodeAt(n)
        if (r < 128) {
          t += String.fromCharCode(r)
          n++
        } else if (r > 191 && r < 224) {
          // eslint-disable-next-line no-undef
          c2 = e.charCodeAt(n + 1)
          // eslint-disable-next-line no-undef
          t += String.fromCharCode(((r & 31) << 6) | (c2 & 63))
          n += 2
        } else {
          // eslint-disable-next-line no-undef
          c2 = e.charCodeAt(n + 1)
          // eslint-disable-next-line no-undef
          c3 = e.charCodeAt(n + 2)
          // eslint-disable-next-line no-undef
          t += String.fromCharCode(
            ((r & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63)
          )
          n += 3
        }
      }
      return t
    },
    updateCollapse() {
      this.$store.commit('updateCollapse')
    },
    logout() {
      // localStorage.removeItem('user');
      // this.props.history.push('/login');
      var _back = encodeURIComponent(window.location.href)
      window.location.href =
        appConfig.loginUrl + '?backUrl=' + _back + '&loginOut=1'
    }
  },
  mounted() {
    const userCookie = this.getCookies('codo_nickname')
    this.userName = userCookie ? this.baseDecode(userCookie) : ''

    this.$store.commit('updateUserName', this.userName)
  }
}
</script>
<style lang="less" scoped>
.home {
  height: 100vh;
  position: absolute;
  left: 200px;
  right: 0;
  top: 0;
  bottom: 0;
  background: #f1f2f5;
  overflow-y: scroll;
}

.home-close {
  height: 100vh;
  position: absolute;
  left: 60px;
  right: 0;
  top: 0;
  bottom: 0;
  background: #f1f2f5;
  overflow-y: scroll;
}
.home-iframe{
  height: 100vh;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: #f1f2f5;
  overflow-y: scroll;
}
.home-top {
  display: flex;
  width: 100%;
  justify-content: space-between;
  height: 50px;
  align-items: center;
  background: #fff;

  i {
    font-size: 20px;
    margin-left: 20px;
  }

  .el-dropdown-box {
    margin-right: 30px;
  }
}

.contain {
  padding: 20px;
  background: #fff;
  margin-top: 5px;
  margin-bottom: 10px;
}

.header-right {
  display: flex;
  align-items: center;
}

::v-deep.el-dropdown-menu__item {
  padding: 0;
}

.drop-item {
  padding: 0 20px;
  min-width: 65px;
  text-align: center;
}
</style>
```

子组件添加监听事件：
```vue
  watch: {
    '$store.state.scrollTop'() {
      let scrollHeight = this.$store.state.scrollHeight
      let scrollTop = this.$store.state.scrollTop
      let containerHeight = this.$store.state.clientHeight
      const distanceToBottom = scrollHeight - (scrollTop + containerHeight)

      // 列表中数据大于等于页面总条数，则不请求数据
      if (this.pageDataNum >= this.pageTotal) {
          return
      }
      if (distanceToBottom <= 50 && this.pagingType) {
        console.log('距离底部还有50px, 当前滚动高度:', scrollTop)
        this.queryLog(this.tabsIndex, null, false, true)
      }
    },
    pagingType(newVal) {
        this.$store.commit('updatePagingType', newVal)
    },
    isBtnOrScrollClick (val) {
      this.$store.commit('updateClickType', val)
    },
    pageDataNum(val) {
      this.$store.commit('updatePageDataNum', val)
      this.$store.commit('updatePageTotal', this.pageTotal)
    }
  },
```