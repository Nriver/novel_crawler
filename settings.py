import platform

# calibre设置
USE_CALIBRE = True
CALIBRE_IP = '192.168.1.5:8080'
CALIBRE_LIBRARY_NAME = '文库吧'
CALIBRE_LOGIN = True
# calibre的用户名密码
CALIBRE_USERNAME = 'ck567'
CALIBRE_PASSWORD = 'ck567'
# 电子书重复是否也添加
ADD_WHEN_DUPLICATE = False

# calibre db
USE_CALIBRE_DB = True
sysstr = platform.system()
if(sysstr == "Windows"):
    CALIBRE_DB_PATH = 'E:/soft/program files/Calibre2_64bit/calibredb.exe'
    CALIBRE_LIBRARY_PATH = 'i:/data/书库/文库吧/'
elif(sysstr == "Darwin"):
    CALIBRE_DB_PATH = '/Applications/calibre.app/Contents/MacOS/calibredb'
    CALIBRE_LIBRARY_PATH = '~/书库/文库吧/'
else:
    CALIBRE_DB_PATH = ''
    CALIBRE_LIBRARY_PATH = ''
