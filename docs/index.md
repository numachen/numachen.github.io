# 欢迎来到【名笔记】！

**关于我**：九零后，自嘲驽马，2015年毕业，2016年加入互联网公司。虽然，本科学的机械设计，却，阴差阳错走上了程序员的道路，便开启了我的升级打怪之旅。一路走来，Python、Vue、Node、Go、DevOPS、云原生、微服务、运维，一路走来，一路学习。做过监控系统、发布系统、运维平台等系统。现把自己所学所悟整理成【名笔记】。


## **关于本站是如何搭建的？**

### 准备工作
- 可以访问外网的梯子
- 自己的GitHub账号
- 自己的域名（不是必须）

### 搭建过程
- 首先阅读下面文章：
      1. https://sspai.com/post/54608
- 我使用的是GitHub Pages方式构建管理自己的网站
     1. 新建一个GitHub仓库，仓库名为numachen.github.io，其中numachen是你的GitHub用户名（numachen.github.io这个域名也将是网站的访问域名）
     2. 将仓库克隆到本地，继续阅读下面的步骤
- 网站模板使用的是[mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/)
     1. mkdocs-material是一个基于Material Design的静态网站生成器，它支持Markdown语法，并且提供了丰富的主题和插件，可以方便地生成美观的网站
     2. mkdocs-material的安装和使用都非常简单，只需要在本地安装Python和pip，然后使用pip安装mkdocs-material即可
     3. 我直接复制已有的主题[create-blog](https://github.com/mkdocs-material/create-blog)，在此基础上修改调整的
     4. 更多主题访问网站[catalog](https://github.com/mkdocs/catalog?tab=readme-ov-file#-theming) 
     5. 将create-blog项目放到numachen.github.io目录下
           - `pip install mkdocs-material` 
           - `mkdocs serve`
     6. 打开浏览器，访问http://127.0.0.1:8000/，就可以看到网站的效果了
- 将网站部署到GitHub Pages上
    1. 本地仓库新建[.github/workflows/static.yml](https://github.com/numachen/numachen.github.io/blob/main/.github/workflows/static.yml)文件，这个是github action，触发自动流水线
    2. 本地编译： `mkdocs build`
    3. 代码上传： `git push`
    4. 等待GitHub Pages自动部署，访问https://numachen.github.io/，就可以看到网站的效果了
    5. 因为我有自己的域名，所以，还需要将域名解析到GitHub Pages上，域名解析到GitHub Pages上，需要将域名解析到GitHub Pages的IP地址上，这个IP地址可以通过网络拨测工具获取，比如阿里云的[网络拨测工具](https://boce.aliyun.com/detect/dns?spm=a2c1d.8251892.domain-setting.ddetect.5f925b766INRvG&target=www.mingnotes.org.cn&type=CNAME)
- 完成以上，你就拥有自己的网站了！当然方式有很多种，模板也有很多，各位就自己发挥吧！
