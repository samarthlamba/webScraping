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
                CREATE TABLE paper_data(
                    title BLOB,
                    authors BLOB,
                    published_date BLOB,
                    doi BLOB,
                    abstract BLOB,
                    publication_location BLOB,
                    link BLOB
                )
            ''')
                    # citations BLOB,
                    # readership BLOB,
                    # tweets BLOB,
                    # news_mentions BLOB
                    
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
    
    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
            # INSERT INTO paper_data(title, authors, published_date, doi, abstract, publication_location, link, citations, readership, tweets, news_mentions) VALUES (?,?,?,?,?,?,?,?,?,?,?)

        self.c.execute('''
            INSERT INTO paper_data(title, authors, published_date, doi, abstract, publication_location, link) VALUES(?,?,?,?,?,?,?)
        ''', (
            item.get('title'),
            item.get('authors'),
            item.get('published_data'),
            item.get('doi'),
            item.get('abstract'),
            item.get('publication_location'),
            item.get('link')
            # item.get('citations'),
            # item.get('readership'),
            # item.get('tweets'),
            # item.get('news_mentions')
        ))
        self.connection.commit()
        return item