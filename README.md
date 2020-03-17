# novel_crawler
Download novel from online website with scrapy.
It can download novel from https://www.wenku8.net and generate epub file. If the online novel contains scanned illustrate pictures, this program will download them and add to the epub file, too.
After generating the epub, you can optionally add the epub to a [Calibre](https://calibre-ebook.com/) content server.

# how to use
In cmd type follows:
```
scrapy crawl novel -a no=NOVEL_ID
```
The NOVEL_ID is the id number of the manga on the wenku8 site.
eg. For novel "BACCANO!", it is 218, so the command would be like this:
```
scrapy crawl novel -a no=218
```

Change settings.py for Calibre settings.

Notice, if Calibre does not have a authentication, the enable-local-write in sharing config need to be enabled.