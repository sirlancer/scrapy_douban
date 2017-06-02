# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import csv

class ScrapyDoubanPipeline(object):
    def process_item(self, item, spider):
    	with codecs.open('movies.csv','a',encoding='utf-8') as f:
    		csv_writer = csv.writer(f,delimiter=',')
    		header = item.keys()
    		if not self.exsist_header:
    			csv_writer.writerow(header)
    			self.exsist_header = True
    		data = item.values()
    		csv_writer.writerow(data)
    	return item
    exsist_header = False