# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from wenku8.items import VolumnItem, ChapterItem
from bs4 import BeautifulSoup


class Wenku8Pipeline(object):

    def process_item(self, item, spider):
        # print u'执行 pipeline'
        if isinstance(item, ChapterItem):
            # print u'处理章节'
            volumn_index = item['volumn_index']
            chapter_index = item['chapter_index']
            chapter_content = item['chapter_content']
            # 解析页面
            soup_detail = BeautifulSoup(chapter_content, 'lxml', from_encoding='utf-8')
            # 删掉广告元素
            [x.extract() for x in soup_detail.find_all('ul', id='contentdp')]

            novel_no = item['novel_no']
            print u'写入文件 卷数%s 章节%s ' % (volumn_index, chapter_index)
            # 创建文件夹
            volumn_folder = os.getcwd().replace('\\', '/') + '/' + str(novel_no) + '/' + str(volumn_index)
            chapter_file_path = str(volumn_folder) + '/' + str(chapter_index) + '.html'
            if not os.path.exists(volumn_folder):
                try:
                    os.makedirs(volumn_folder)
                except:
                    pass
            # 写文件
            with open(chapter_file_path, 'wb') as f:
                f.write(unicode(soup_detail.prettify()))


class GenerateEpubPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, VolumnItem):
            # print u'处理一卷书'
            volumn_index = item['volumn_index']
            print u'生成 卷数%s 的epub' % volumn_index

        # 这里不return也可以
        return item
