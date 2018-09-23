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
from ebooklib import epub


class Wenku8Pipeline(object):

    def process_item(self, item, spider):
        # 预订删除
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
            volumn_folder = os.getcwd().replace('\\', '/') + '/download/' + str(novel_no) + '/' + str(volumn_index)
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

    @staticmethod
    def prettify_html(page_content):
        # 简单替换
        replace_word_list = [u'\r\n', u'\xa0', u'&nbsp;', u'&amp;nbsp;']
        for replace_word in replace_word_list:
            page_content = page_content.replace(replace_word, ' ')
        # 解析页面
        soup_detail = BeautifulSoup(page_content, 'lxml', from_encoding='utf-8')
        # 删掉广告元素
        [x.extract() for x in soup_detail.find_all('ul', id='contentdp')]
        return unicode(soup_detail.prettify())

    def process_item(self, item, spider):
        if isinstance(item, VolumnItem):
            # print u'处理一卷书'
            volumn_index = item['volumn_index']
            volumn = item['volumn']
            novel_info = item['novel_info']
            print item['volumn']['chapters'][0][2][:100]
            print u'生成 卷数%s 的epub' % volumn_index

            # 生成epub
            book = epub.EpubBook()
            book.set_title(novel_info['novel_name'])
            book.set_language('zh')
            book.add_author(novel_info['novel_author'])
            # basic spine
            book.spine = ['nav']
            for index, chapter in enumerate(item['volumn']['chapters']):
                c = epub.EpubHtml(title=chapter[0], file_name='Text/%s.xhtml' % index, lang='zh')
                c.content = item['volumn']['chapters'][index][2]
                c.content = self.prettify_html(c.content)
                book.add_item(c)
                book.toc.append(epub.Link('Text/%s.xhtml' % index, chapter[0], chapter[0]))
                book.spine.append(c)
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            epub_folder = os.getcwd().replace('\\', '/') + '/download/' + novel_info['novel_no']
            epub_path = epub_folder + '/' + str(volumn_index) + '.epub'
            if not os.path.exists(epub_folder):
                try:
                    os.makedirs(epub_folder)
                except:
                    pass

            epub.write_epub(epub_path, book, {})

        # 这里不return也可以
        return item
