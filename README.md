# jinritoutiao-images
今日头条搜索“街拍”图片抓取并入库

----------

## 目标 ##

●获取今日头条搜索的keyword下的所有结果组图

●获取图片地址

●下载图片

●使用多进程

●了解AJAX抓取

## 主要用到的库： ##
```
requests
re
pymongo
multiprocessing 
BeautifulSoup
json
```

## 入口 ##

url：https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3

![](https://i.imgur.com/aaYfmr3.png)

第一：

根据上图分析，看到套图的地址是article_url,通过AJAX获取消息

第二：

页面搜索结果是根据offset的值来变化的，所以我们可以构造offset值的变化来获取更多的搜索结果

## 分析url： ##


通过对url列表套图地址的分析，我们可以发现有两种类型的组图

第一种是和文章一起的：

![](https://i.imgur.com/yBupDBL.png)

第二种通过gallery显示：

![](https://i.imgur.com/PlHDdxC.png)



> ## mongodb数据库显示结果： ##

![](https://i.imgur.com/kAh4c0e.jpg)

> ## 下载的图片： ##

![](https://i.imgur.com/U8uLxII.jpg)

> ## 输出的结果： ##

![](https://i.imgur.com/knI3IoZ.png)