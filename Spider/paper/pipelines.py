# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os


class PaperPipeline:
    def open_spider(self, spider):
        """Spider ON"""
        self.file = open('File_name.csv', 'a', encoding='utf-8')
        
    def close_spider(self, spider):
        """Spider OFF"""
        self.file.close()
    
    def process_item(self, item, spider):
        """item Pipeline"""
        line = f"{item['doi']},{item['file_name']}\n"
        self.file.write(line)
        return item
