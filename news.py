
# coding: utf-8

# In[11]:


import requests
import json
from bs4 import BeautifulSoup
import pandas

commentUrl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'

urlPage = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&_=1523862495258'

totalLink = []

#获取新闻的评论信息
def getComment(newsUrl):
    newsId = newsUrl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
    comment = requests.get(commentUrl.format(newsId))
    jd = json.loads(comment.text)
    return jd['result']['count']['total']

#获取新闻的概要信息
def getNewInfo(newUrl):
    newInfo = {}
    res = requests.get(newUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    newInfo['title'] = soup.select('.main-title')[0].text
    newInfo['date'] = soup.select('.date-source .date')[0].text
    newInfo['source'] = soup.select('.date-source .source')[0].text
    newInfo['author'] = soup.select('.show_author')[0].text.lstrip('责任编辑 ：')
    newInfo['content'] = '@'.join([ p.text.strip() for p in soup.select('.article p')[:-1]])
    newInfo['comment'] = getComment(newUrl)
    return newInfo

#获取新闻的link
def getParseLink(newsUrl):
    link = []
    res = requests.get(newsUrl)
    jd = json.loads(res.text)
    datas = jd['result']['data']
    for data in datas:
        link.append(getNewInfo(data['url']))
    return link


#获取前4页新闻信息
for page in range(1,5):
    totalLink.extend(getParseLink(urlPage.format(page)))
print(len(totalLink))

#用pandas分析数据
df = pandas.DataFrame(totalLink)
df.head(10)

#生成excle文件
df.to_excel('news.xlsx')


# In[5]:




