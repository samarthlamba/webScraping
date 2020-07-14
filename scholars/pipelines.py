# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sqlite3

class SQLlitePipeline(object):    
    def open_spider(self, spider):
        self.connection = sqlite3.connect("articles.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE paper(
                    title TEXT,
                    authors TEXT,
                    doi TEXT
                )
            ''')
                        # citations BLOB,
                        # readership BLOB,
                        # tweets BLOB,
                        # news_mentions BLOB
                        
            self.connection.commit()
        except sqlite3.OperationalError:
            pass




    def process_item(self, item, spider):
        print("Types_all")
        print(type(item.get('title')))
        print(type(item.get('authors')))
        print(type(item.get('doi')))
        self.c.execute('''
        INSERT INTO paper (title, authors, doi) VALUES(?, ?, ?)
        ''', (
            item.get('title'),
            item.get('authors'),
            item.get('doi'),
        ))
        self.connection.commit()
        logging.warning("SPIDER PROCESSED")
        return item

    def close_spider(self, spider):
        self.connection.close()



import json

from itemadapter import ItemAdapter

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item