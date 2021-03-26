# -*- coding:utf8 -*-
import sys
import io
import mysql.connector
import datetime
from requests_html import HTMLSession

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码

# 创建数据库链接，创建游标
conn = mysql.connector.connect(user='root', password='123456', database='test', charset='utf8')
cursor = conn.cursor()

# 创建会话，get请求，获取标题列表
session = HTMLSession()
r = session.get('http://www.pingcheng.gov.cn/pcqrmzf/zcfw/list_2.shtml')
titles = r.html.find('.news_list.page_list > li > a')

# 编写sql
datalist = []
sql = "insert into table_text (title,url,create_time,content,source,publishDate) values (%s,%s,%s,%s,%s,%s);"

# 从标题列表中循环爬取
for title in titles:
    mytitle = title.text.encode('utf-8')
    myurl = list(title.absolute_links)[0]  # 获取爬取绝对路径
    # myurl = ((str(title.absolute_links).replace('{', '')).replace('}', '')).replace('\'', '')
    create_time = datetime.datetime.now()
    connectSession = session.get(myurl)  # get请求获取HTML页面
    source = list(connectSession.html.xpath('//span[2]/text()'))[0]
    mysouce = source.replace("来源：", "")
    publishDate = list(connectSession.html.xpath('//span[1]/text()'))[0]
    mydate = publishDate.replace("发布时间：", "")
    contents = ''
    connect = connectSession.html.find('body > div > div.main_body.main_content.clearfix > div.content')
    for connectText in connect:
        text = connectText.text
        contents += text
    datalist.append((mytitle, myurl, create_time, contents, mysouce, mydate))
cursor.executemany(sql, datalist)  # 执行sql语句
conn.commit()  # 提交到数据库执行
cursor.close()  # 关闭游标
conn.close() # 关闭数据库连接
