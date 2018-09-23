# novel_crawler
Download novel from online website with scrapy.
The aim is to download novel from https://www.wenku8.net and generate epub file.
Then, if possible add the epub to local library.

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