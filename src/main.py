import requests as rq
from bs4 import BeautifulSoup

import win32api,win32con,win32gui,os,random,time

print('作者：Himpq')

ids = {
    'anime':1,
    'animegirls':5
}

idCh = 'https://wallhaven.cc/search?q=id:%s&ref=fp&page=%s'
seCh = 'https://wallhaven.cc/search?q=%s&page=%s'

a='https://w.wallhaven.cc/full/eo/wallhaven-eozq2o.jpg'
b='https://th.wallhaven.cc/small/eo/eozq2o.jpg'

n=1

def smallToFull(link):
    l = link.split('/')[-1]
    tp = link.split('/')[4]

    return 'https://w.wallhaven.cc/full/%s/wallhaven-%s' % (tp,l)

def getTypeURL(type_,page):
    if type_ in ids:
        rtn = idCh % (ids[type_],page)
    else:
        return seCh % (type_.replace(' ','+'),page)

def getUrlSmallPic(text):
    soup = BeautifulSoup(text,'lxml')
    o = list(soup.find_all(attrs={'class':'lazyload'}))
    url = []
    for i in o:
        i = str(i)
        #print(i)
        url.append(smallToFull(i.split('"')[5]))

    return url

def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key,"WallpaperStyle",0,win32con.REG_SZ,'2')
    win32api.RegSetValueEx(key,"TileWallpaper",0,win32con.REG_SZ,'0')
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,path,1+2)

def Spider(search,page,downnum):
    global n
    i = rq.get(getTypeURL(search,page))
    c=getUrlSmallPic(i.text)
    n = len(c)

    a=downnum
    if len(c) < a:
        print('错误.')
    else:
        j = c[a]
        f = rq.get(j).content

        path = 'C:/temp/%s.jpg' % j.split('/')[-1]
        
        with open(path,'wb') as file:
            file.write(f)

        print('已经自动设置为桌面壁纸')

s=input('搜索:') #搜索图片
p=input('页码:') #爬取页码
d=0

while d < n:
    Spider(s,p,d)

    d += 1
    time.sleep(60)  #隔多少秒换一次
