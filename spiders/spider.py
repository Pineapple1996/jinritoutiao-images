import json
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import re
from jinritop.config import *
import pymongo
from hashlib import md5
import os
from multiprocessing import Pool

#建立mongodb连接
conn = pymongo.MongoClient(MONGO_URL)
db=conn[MONGO_DB]


#获取原始页面源码
def get_html_index(offset,keyword):
    data = {
        'offset':offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)  #编码url传递数据
    response = requests.get(url)    #请求原始页面数据
    try:
        if response.status_code == 200: #判断状态码
            return response.text
        return  None
    except RequestException:    #捕获异常
        print('请求索引页出错!')
        return None


#解析原始页面源码，提取详情页url（详情页url生成器）
def parse_index_html(html):
    data =json.loads(html)  #解析json
    if data and 'data' in data.keys(): #判断data是否存在
        for item in data.get('data'):
            yield item.get('article_url')   #生成详情页url


 #获取详情页源码
def get_url_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错!')
        return None

#解析详情页
def parse_detail_url(html,url):
    soup= BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()    #获取组图标题
    print(title)
    parttan=re.compile('gallery: JSON.parse\((.*?)\),',re.S)    #第一种组图匹配正则表达式
    results=re.search(parttan,html)
    if results:
        # print(results.group(1))
        data = json.loads(json.loads(results.group(1)))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item['url'] for item in sub_images]
            for image in images:
                download_images(image)  #下载图片
            return {
                'title':title,
                'url':url,
                'images':images
            }
    else:
        parttan2 = re.compile('img src&#x3D;&quot;(.*?)&quot;', re.S)   #第二种组图匹配正则表达式
        images2 = re.findall(parttan2, html)
        for image in images2:
            download_images(image)  #下载图片
        return {
            'title': title,
            'url': url,
            'images': images2
        }

#将图片url存入mangodb
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功')
        return True
    return False

#下载图片
def download_images(url):
    print('正在下载：'+url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('下载图片出错!')
        return None

#将图片存到文件夹
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+'\images',md5(content).hexdigest(),'jpg')
    if  not os.path.exists(file_path):  #去重
        with open(file_path,'wb') as f:
            f.write(content)


def main(offset):
    html = get_html_index(offset,KEYWORD)
    for urls in parse_index_html(html):
        if urls:
            html = get_url_detail(urls)
            result = parse_detail_url(html,urls)
            # print(result)
            save_to_mongo(result)


if __name__ == '__main__':

    group=[i*20 for i in range(START,END+1)]
    # main(0,KEYWORD)
    pool=Pool()
    pool.map(main,group)    #开启多进程