# 简单爬虫 #

最近比较闲,爬些感兴趣的博文来看(python golang等)

# 关键字 #

因为blog网站自带搜索过滤关键字功能,所以省去了关键字匹配  
python(可在url里替换)

# 来源 #

- oschina  
    `http://www.oschina.net/search?q=python&scope=blog&sort_by_time=1&p=1`  

- csdn  
    `http://blog.csdn.net/tag/details.html?tag=python&page=1`

- v2ex  
    `http://www.v2ex.com/go/python?p=1`

- cnblogs  
    `http://www.cnblogs.com/cate/python/#p1`

# 终止条件 #

当遇到blog id已经存在时,说明后面的blog已经爬过,终止本次爬取,等待下次

# 配置 #

`spider/etc/blog/default.json`

# database设计(mongodb -- spider) #

- blog

        {
            "src":"", # 来源: 'oschina', 'csdn', 'v2ex', 'cnblogs'
            "title":"",
            "link":"", #博客链接,唯一索引
            "date":"", # '%Y-%m-%d'
            "author":"",
            "summary":"",
            "spider_date":"" # '%Y-%m-%d %X'
        }

# 测试使用 #

进入 `spider-blog` 目录  
`python spider --loglevel WARN --settings etc/blog/default.json`