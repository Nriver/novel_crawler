# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChapterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 小说名称
    novel_name = scrapy.Field()
    # 小说编号
    novel_no = scrapy.Field()
    # 作者
    novel_author = scrapy.Field()
    # 第几卷
    volumn_index = scrapy.Field()
    # 卷的名称
    volume_name = scrapy.Field()
    # 章节名称
    chapter_name = scrapy.Field()
    # 章节序号
    chapter_index = scrapy.Field()
    # 章节内容
    chapter_content = scrapy.Field()

    pass


class VolumnItem(scrapy.Item):
    # 小说信息
    novel_info = scrapy.Field()
    # 第几卷
    volumn_index = scrapy.Field()
    # 小说某卷的内容
    volumn = scrapy.Field()

    # # 小说名称
    # novel_name = scrapy.Field()
    # # 小说编号
    # novel_no = scrapy.Field()
    # # 作者
    # novel_author = scrapy.Field()
    # # 卷的名称
    # volume_name = scrapy.Field()
    # # 章节顺序
    # chapters = scrapy.Field()

    pass
