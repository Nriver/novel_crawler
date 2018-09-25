# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2018-09-23 20:12:01
# @Last Modified by:   Zengjq
# @Last Modified time: 2018-09-25 13:30:28
# Define here the models for your scraped items
#
# See documentation in
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChapterItem(scrapy.Item):
    """
    章节 item
    """
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

    def __repr__(self):
        """
        防止日志输出过多内容
        控制只输出部分信息
        """
        """only print out attr1 after exiting the Pipeline"""
        return repr({"volumn_index": self['volumn_index']})


class VolumnItem(scrapy.Item):
    """
    卷 item
    """
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
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({"volumn_index": self['volumn_index']})


class ImageItem(scrapy.Item):
    """
    图片 item
    ImagePileline的item需要两个参数
    1.image_urls 用来下载图片
    2.image_paths 用来保存下载的图片路径
    """
    # 网络路径
    image_urls = scrapy.Field()
    # 下载后的图片对象
    images = scrapy.Field()
    # 卷 item
    volumn_item = scrapy.Field()
    # 图片存储路径
    image_paths = scrapy.Field()
    # flag
    download_finish_flag = scrapy.Field()

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({"image_urls": self['image_urls']})
