# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Demo1Pipeline:
    def process_item(self, item, spider):
        return item

class LottoInsertPipeline:
    def process_item(self, item, spider):

        from .items import WinningNumbersInfo

        if type(item) is WinningNumbersInfo:

            import pymysql
            conn = pymysql.connect(host='localhost',
                                   database='pydemodb',
                                   user='ssacuser',
                                   password='ssac123!@#',
                                   charset='utf8')

            with conn.cursor() as cursor:
                sql = """
                insert into table_lotto (rnd, no1, no2, no3, no4, no5, no6, bno) values(%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, item.to_list())

                conn.commit()

            conn.close()

        return item  # 다음 파이프라인으로 전달 (필수)

class LottoDupCheckPipeline:
    def process_item(self, item, spider):

        from .items import WinningNumbersInfo
        from scrapy.exceptions import DropItem

        if type(item) is WinningNumbersInfo:

            import pymysql
            conn = pymysql.connect(host='localhost',
                                   database='pydemodb',
                                   user='ssacuser',
                                   password='ssac123!@#',
                                   charset='utf8')

            with conn.cursor() as cursor:
                sql = """
                select count(*) from table_lotto where rnd=%s
                """
                cursor.execute(sql, item['rnd'])

                row = cursor.fetchone()

                if row[0] != 0: # 중복 데이터
                    raise DropItem('duplicated item')

            conn.close()

        return item  # 다음 파이프라인으로 전달 (필수)