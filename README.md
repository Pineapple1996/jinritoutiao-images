# jinritoutiao-images
今日头条搜索“街拍”图片抓取并入库

----------

## 主要用到的库： ##
```
requests
re
pymongo
multiprocessing 
BeautifulSoup
json
```


## 分析url： ##

url：https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3

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