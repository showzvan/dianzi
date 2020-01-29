# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "123456",
        # charset = "utf-8",
        use_unicode = False
    )
    return conn

class XianhuoPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE xianhuo")
        # 插入数据库
        sql = "INSERT INTO xianhuospider(model,price,shop,status,levels,brand) VALUES(%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql,
                           (item["model"],item["price"],item["shop"],item["status"],item["levels"],item["brand"]))
            cursor.connection.commit()
            print("写入成功")
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        return item
