# 网站数据抓取二次开发框架
基于scrapy的二次开发框架，通过简单配置，即可实现一个网站分类中所有项目指定信息的抓取<br>
常驻式进程，启动之后，通过feed投放任务，使用redis实现分布式，多台机器多个爬虫实时监控任务抓取

## 需要掌握技能
- xpath表达式，正则表达式，以及css表达式，至少会其中一项
- python 字典和列表数据结构
## 以下技能最好掌握
- python lambda 表达式的使用
- python 简单函数编写
- 了解scrapy的基本概念，参见[wiki](https://github.com/ShichaoMa/webWalker/wiki)

# INSTALL
## ubuntu && windows
```
git clone https://github.com/ShichaoMa/webWalker.git

or

(sudo) pip install web-walker
```

# HELLOWORLD
### 1 安装完毕后（推荐pip安装）使用scrapy生成一个项目
```
ubuntu@dev:~/myprojects$ scrapy startproject demo
New Scrapy project 'demo' created in:
    /home/ubuntu/myprojects/demo

You can start your first spider with:
    cd demo
    scrapy genspider example example.com


# 目录结构如下
.
├── demo
│   ├── __init__.py
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       └── __init__.py
└── scrapy.cfg

```

### 1 或者直接从test中复制[myapp](https://github.com/ShichaoMa/webWalker/tree/master/test)，如果要改项目名字，记得修改scarpy.cfg中的名字

### 2 删除掉其中的demo/items.py demo/piplines.py，并使用myapp/settings.py，myapp/spipders/__init__.py 替掉原来的文件

### 3 在spiders目录下，创建page_xpath.py, item_xpath.py, item_field.py, spiders.py，编写以下内容
```
# spiders.py

# -*- coding:utf-8 -*

SPIDERS = { # 配置spider, spider名称一个字典，字典中为这个spider的一些自定义属性，可为空
    "bluefly": {}
}

# page_xpath.py

# -*- coding:utf-8 -*

PAGE_XPATH = { # 配置网站分类页中获取下一页链接的方式，具体策略参见wiki
    "bluefly": [
        '//*[@id="page-content"]//a[@rel="next"]/@href',
    ]
}

# item_xpath.py

# -*- coding:utf-8 -*

ITEM_XPATH = { # 配置网站分类页中获取商品页链接的方式，xpath表达式
    "bluefly": [
        '//ul[@class="mz-productlist-list mz-l-tiles"]/li//a[@class="mz-productlisting-title"]/@href',
    ]
}

# item_field

# -*- coding:utf-8 -*

ITEM_FIELD = { # 商品页中，所需信息的获取方式，具体策略参见wiki
    "bluefly": [
        ('product_id', {
            "xpath": [
                '//li[@itemprop="productID"]/text()',
            ],
        }),
        ('brand', {
            "xpath": [
                '//p[@class="mz-productbrand"]/a/text()',
            ],
        }),
        ('names', {
            "xpath": [
                '//span[@class="mz-breadcrumb-current"]/text()',
            ],
        }),
    ]
}

```
### 4 修改demo/settings.py 文件，或者直接新建localsettings.py，增加自定义配置，要修改的项目在settings.py已注明

### 5 启动redis
```
#如果没有安装redis，可以使用自带的custom-redis，配置文件中需写明CUSTOM_REDIS=True
custom-redis-server -p 6379

```
### 6 启动爬虫
```
cd demo
scrapy crawl bluefly

```
### 7 投放任务
```
# 使用自带的costom-redis 需要加上 --custom
feed -c test_01 -s bluefly -u "http://www.bluefly.com/assortment/the-boot-shop-overarching/women/shoes" --custom
```

# DECUMENT
参见[wiki](https://github.com/ShichaoMa/webWalker/wiki)
