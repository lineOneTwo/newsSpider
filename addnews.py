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
for row in results:
    title = row[0]
    content = row[1]
    source = row[2]
    publishDate = row[3]
    # 打印结果
    # print("title=%s,content=%s,source=%s,publishDate=%s" %
    #       (title, content, source, publishDate))
    url = 'http://zspctst.wt.com:14331/hand-city-web/manage/zsNews/doSave'
    headers = {
        'Cookie': 'SESSION=OGE5ZmM3NTAtNDg2Ny00YmZhLWI4YTQtNzVmMjY3MDY5M2U3'
    }
    data = {
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
    response = requests.post(url, headers=headers, data=data)
    print(response.text)
