# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2018-09-23 20:12:01
# @Last Modified by:   Zengjq
# @Last Modified time: 2020-03-15 21:32:03
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from wenku8.items import VolumnItem, ChapterItem, ImageItem
from bs4 import BeautifulSoup
from ebooklib import epub
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import requests
from requests.auth import HTTPDigestAuth
import subprocess
import platform


class Wenku8Pipeline(object):

    def process_item(self, item, spider):
        # 预订删除
        print('执行 pipeline')
        if isinstance(item, ChapterItem):
            print('处理章节')
            volumn_index = item['volumn_index']
            chapter_index = item['chapter_index']
            chapter_content = item['chapter_content']
            # 解析页面
            soup_detail = BeautifulSoup(chapter_content, 'lxml', from_encoding='utf-8')
            # 删掉广告元素
            [x.extract() for x in soup_detail.find_all('ul', id='contentdp')]

            novel_no = item['novel_no']
            print('写入文件 卷数%s 章节%s ' % (volumn_index, chapter_index))
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
                f.write(soup_detail.prettify())
        # 这个return是很重要的
        # 如果不return 下一个pipeline就收不到item
        return item


class ImageDownloadPipeline(ImagesPipeline):
    """
    先下载图片
    然后生成epub
    """

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
        return soup_detail.prettify()

    @staticmethod
    def get_cover_image(page_content):
        soup_detail = BeautifulSoup(page_content, 'lxml', from_encoding='utf-8')

    @staticmethod
    def uplaod_book_to_calibre(book_path, calibre_ip, username, password, calibre_library_name, add_when_duplicate=False):
        calibre_library_name = requests.utils.requote_uri(calibre_library_name)
        """
        给calibre添加电子书
        """
        add_when_duplicate = {True: 'y', False: 'n'}[add_when_duplicate]
        url = 'http://' + calibre_ip + '/cdb/add-book/1/' + add_when_duplicate + '/0.epub/' + calibre_library_name
        files = {
            # 文件名可以随便取 关键的是路径不要出错
            'file': ('0.epub', open(book_path, 'rb')),
        }

        # calibre用的认证是DigestAuth
        response = requests.post(url, data=None, files=files, auth=HTTPDigestAuth(username, password))
        if response.status_code == 200:
            print('文件添加成功')
        else:
            print('文件 %s 添加失败' % book_path)
        # print response.text

    @staticmethod
    def uplaod_book_to_calibre_by_calibre_db(book_path, calibre_ip, username, password, calibre_library_name, add_when_duplicate=False, calibre_db_path=''):
        # calibre_library_name = requests.utils.requote_uri(calibre_library_name)
        """
        给calibre添加电子书
        """
        sysstr = platform.system()
        if(sysstr == "Windows"):
            calibre_library_path = 'http://' + calibre_ip + '/#' + calibre_library_name
            cmds = [calibre_db_path, 'add', '--with-library', calibre_library_path, '--password', password, '--username', username]
            if add_when_duplicate:
                cmds.append('--duplicates')
            cmds.append(book_path)
            print(' '.join(cmds))
            subprocess.call(cmds, shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
        else:
            # mac下转义 '\#'
            calibre_library_path = 'http://' + calibre_ip + '/\#' + calibre_library_name
            cmds = [calibre_db_path, 'add', '--with-library', calibre_library_path, '--password', password, '--username', username]
            if add_when_duplicate:
                cmds.append('--duplicates')
            cmds.append(book_path)
            print(' '.join(cmds))
            # mac 一定要用join后的命令 传list进去执行不了
            subprocess.call(' '.join(cmds), shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)

    # pic.wkcdn.com 有反爬虫机制
    # 不遵守robot.txt
    # header可以不要
    # 如果要添加 一定不能加referer 有referer就会被屏蔽

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'DNT: 1': 1,
        'Host': 'pic.wkcdn.com',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    default_headers = {}

    def get_media_requests(self, item, info):
        if isinstance(item, ImageItem):
            print('下载卷 %s 的图片' % str(item['volumn_item']['volumn_index']))
            for image_url in item['image_urls']:
                # 拼一下图片存储的路径
                novel_no = item['volumn_item']['novel_info']['novel_no']
                novel_name = item['volumn_item']['novel_info']['novel_name']
                volumn_index = item['volumn_item']['volumn_index']
                file_name = image_url.split('/')[-1]
                file_store_path = novel_no + '_' + novel_name + '/Images/' + str(volumn_index) + '/' + file_name
                print('图片下载路径', image_url)
                print('图片保存路径', file_store_path)
                yield scrapy.Request(image_url, meta={'file_store_path': file_store_path}, headers=self.default_headers)
                # yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None):
        return request.meta['file_store_path']

    def item_completed(self, results, item, info):
        # 书里所有的图片
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths

        item['download_finish_flag'] = True
        # return item
        # # 已经遍历完所有的章节 可以对某一卷进行合并了
        volumn_item = item['volumn_item']

        novel_no = item['volumn_item']['novel_info']['novel_no']
        volumn_index = volumn_item['volumn_index']
        volumn = volumn_item['volumn']
        novel_info = volumn_item['novel_info']
        # print volumn_item['volumn']['chapters'][0][2][:100]
        print('卷数%s图片下载完成 生成epub' % volumn_index)

        # 生成epub
        book = epub.EpubBook()
        # epub信息名称是小说名称+卷名称
        book.set_title(novel_info['novel_name'] + ' ' + volumn['volumn_name'])
        book.set_language('zh')
        book.add_author(novel_info['novel_author'])
        # basic spine
        book.spine = ['nav']
        # 添加小说文字章节
        for index, chapter in enumerate(volumn_item['volumn']['chapters']):
            c = epub.EpubHtml(title=chapter[0], file_name='Text/%s.xhtml' % index, lang='zh')
            c.content = volumn_item['volumn']['chapters'][index][2]
            c.content = self.prettify_html(c.content)
            book.add_item(c)
            book.toc.append(epub.Link('Text/%s.xhtml' % index, chapter[0], chapter[0]))
            book.spine.append(c)

        # 这里要把所有的插图放到epub里面去
        for image_path in image_paths:
            # epub内的文件路径
            file_name = 'Images/' + image_path.split('/')[-1]
            # 实际图片的完整路径
            file_path = os.getcwd().replace('\\\\', '/') + '/download/' + image_path
            epub_image_item = epub.EpubItem(uid="image", file_name=file_name, content=open(file_path, 'rb').read())
            book.add_item(epub_image_item)
            pass

        # 生成封面图
        if image_paths:
            # 如果有插图 就用第一张插图当封面
            file_name = 'Images/' + image_paths[0].split('/')[-1]
            file_path = os.getcwd().replace('\\', '/') + '/download/' + image_paths[0]
            book.set_cover(file_name, content=open(file_path, 'rb').read(), create_page=True)
        else:
            # 如果某卷一个插图都没有 那就用网站上的缩略图
            import urllib
            cover_url = item['volumn_item']['novel_info']['novel_cover']
            cover_ext = cover_url.split('.')[-1]
            image_folder_path = os.getcwd().replace('\\', '/') + '/download/' + novel_no + '/Images/' + str(volumn_index)
            cover_path = image_folder_path + '/cover.' + cover_ext
            print('下载缩略图 %s 保存路径 %s' % (cover_url, cover_path))
            if not os.path.exists(image_folder_path):
                os.makedirs(image_folder_path)
            try:
                urllib.urlretrieve(cover_url, cover_path)
                print('封面文件已下载', os.path.exists(cover_path))
                book.set_cover('Images/cover.' + cover_ext, content=open(cover_path, 'rb').read(), create_page=True)
            except:
                print('小说 %s 封面下载失败' % book.title)

        # 加入默认的ncx和nav(做什么的?)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # 生成epub文件
        epub_folder = os.getcwd().replace('\\', '/') + '/download/' + novel_info['novel_no'] + '_' + novel_info['novel_name']
        epub_path = epub_folder + '/' + str(volumn_index) + '.epub'
        print('epub存储路径', epub_path)
        if not os.path.exists(epub_folder):
            try:
                os.makedirs(epub_folder)
            except:
                pass
        # 写入epub文件
        epub.write_epub(epub_path, book, {})
        print('写入epub成功')
        # calibre相关
        # 生成epub之后 是否上传到calibre服务器
        settings = get_project_settings()
        use_calibre = settings.get('USE_CALIBRE')
        if use_calibre:
            print('上传到calibre书库')
            use_calibre_db = settings.get('USE_CALIBRE_DB')
            calibre_library_path = settings.get('CALIBRE_LIBRARY_PATH')
            calibre_db_path = settings.get('CALIBRE_DB_PATH')
            calibre_ip = settings.get('CALIBRE_IP')
            calibre_library_name = settings.get('CALIBRE_LIBRARY_NAME')
            # 用户名密码
            calibre_username = settings.get('CALIBRE_USERNAME')
            calibre_password = settings.get('CALIBRE_PASSWORD')
            # 电子书重复是否覆盖
            add_when_duplicate = settings.get('ADD_WHEN_DUPLICATE')

            if use_calibre_db:
                self.uplaod_book_to_calibre_by_calibre_db(epub_path, calibre_ip, calibre_username, calibre_password, calibre_library_name, add_when_duplicate, calibre_db_path)

            else:

                self.uplaod_book_to_calibre(epub_path, calibre_ip, calibre_username, calibre_password, calibre_library_name, add_when_duplicate)
        return item
