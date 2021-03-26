import json
import sys
import io
import requests
import mysql.connector

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码
conn = mysql.connector.connect(user='root', password='123456', database='test', charset='utf8')
cursor = conn.cursor()

# 执行SQL语句
sql = "select title, content, source, publishDate from table_text ;"
cursor.execute(sql)
# 获取所有记录列表
results = cursor.fetchall()


# 查询新闻是否已存在
def selectNews(title):
    selectUrl = 'http://zspctst.wt.com:14331/hand-city-web/manage/zsNews/dataGrid'
    selectHeaders = {
        "Cookie": "SESSION=OGE5ZmM3NTAtNDg2Ny00YmZhLWI4YTQtNzVmMjY3MDY5M2U3",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "Bearer 6d1f8114-91e4-4461-82c8-a677d9d28ac2",
        "Connection": "keep-alive",
        "Content-Length": "301",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Host": "zspctst.wt.com:14331",
        "Origin": "http://zspctst.wt.com:14331",
        "Referer": "http://zspctst.wt.com:14331/readArticleList",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    selectData = {
        "page": "1",
        "limit": "10",
        "status": "1",
        "toped": "",
        "recommend": "",
        "tabId": "c0f6ee4c77824522a7fe035e870b144b",
        "tabName": "动态",
        "title": title,
        "_nickname": "初见",
        "_institution": "系统运维中心",
        "_userType": "超级用户"
    }
    selectResponse = requests.post(selectUrl, headers=selectHeaders, data=selectData)
    results_json = selectResponse.json()
    count = results_json['count']
    print(title, count)
    return count


for row in results:
    title = row[0]
    content = row[1]
    source = row[2]
    publishDate = row[3]
    if selectNews(title) > 0:
        pass
    else:
        print("insert!!!")
        insertUrl = 'http://zspctst.wt.com:14331/hand-city-web/manage/zsNews/doSave'
        insertHeaders = {
            "Cookie": "SESSION=OGE5ZmM3NTAtNDg2Ny00YmZhLWI4YTQtNzVmMjY3MDY5M2U3",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": "Bearer 6d1f8114-91e4-4461-82c8-a677d9d28ac2",
            "Connection": "keep-alive",
            "Content-Length": "301",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "zspctst.wt.com:14331",
            "Origin": "http://zspctst.wt.com:14331",
            "Referer": "http://zspctst.wt.com:14331/readArticleList",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        insertData = {
            "thumb": "",
            "tabId": "c0f6ee4c77824522a7fe035e870b144b",
            "praiseCount": "",
            "content": content,
            "publishDate": publishDate,
            "shareCount": "23",
            "source": source,
            "storeCount": "",
            "title": title,
            "recommend": "0",
            "toped": "0",
            "tabName": "动态",
            "status": "1",
            "_nickname": "初见",
            "_institution": "系统运维中心",
            "_userType": "超级用户"
        }
        response = requests.post(insertUrl, headers=insertHeaders, data=insertData)
        assert response.status_code == 200
