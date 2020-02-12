# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from sshtunnel import SSHTunnelForwarder

def dbHandle():
    with SSHTunnelForwarder(
            ssh_address_or_host=('', 22),  # 指定ssh登录的跳转机的address
            ssh_username='root',  # 跳转机的用户
            ssh_password='',  # 跳转机的密码
            remote_bind_address=('127.0.0.1', 3306)
    ) as server:
        conn = pymysql.connect(
            port=server.local_bind_port,
            host = "127.0.0.1",
            user = "root",
            password = "",
            charset = "utf8",
            db="bijia",
            use_unicode = False
        )
        return conn

class XianhuoPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        # 动态构造
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        try:
            cursor.execute(sql, tuple(data.values()))
            cursor.connection.commit()
            print("写入成功")
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        return item

        # 初始写法
        # dbObject = dbHandle()
        # cursor = dbObject.cursor()
        # # cursor.execute("USE bijia")
        # # 插入数据库
        # sql = "INSERT INTO xianhuospider(model,price,shop,status,levels,brand) VALUES(%s,%s,%s,%s,%s,%s)"
        # try:
        #     cursor.execute(sql,
        #                    (item["model"],item["price"],item["shop"],item["status"],item["levels"],item["brand"]))
        #     cursor.connection.commit()
        #     print("写入成功")
        # except BaseException as e:
        #     print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
        #     dbObject.rollback()
        # return item
