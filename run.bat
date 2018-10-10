@REM @Author: Zengjq
@REM @Date:   2018-10-06 09:27:31
@REM @Last Modified by:   Zengjq
@REM Modified time: 2018-10-06 09:31:03
@echo off
set /p id="Enter ID: "
scrapy crawl novel -a no=%id%
pause()