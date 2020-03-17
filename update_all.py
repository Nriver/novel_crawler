# -*- coding: utf-8 -*-
# @Author: Zengjq
# @Date:   2020-03-16 00:33:51
# @Last Modified by:   Zengjq
# @Last Modified time: 2020-03-16 00:37:55

import os
for x in range(1, 2709):
    os.system('scrapy crawl novel -a no=%s' % x)
