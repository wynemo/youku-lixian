#!/usr/bin/env python

__all__ = ['letv_download']

from common import *
import re, base64, json

#http://www.letv.com/ptv/pplay/5938/1.html

def get_title(s1):
    #get title
    p1 = r'<\s*title\s*>\s*(.*?)\s*<\s*/\s*title\s*>'
    o1 = re.search(p1,s1,re.I|re.S)
    assert(o1)
    title = o1.group(1)
    suffix = ' - \xe5\x9c\xa8\xe7\xba\xbf\xe8\xa7\x82\xe7\x9c\x8b - \xe4\xb9\x90\xe8\xa7\x86\xe7\xbd\x91'
    pos = o1.group(1).rfind(suffix)
    if -1 != pos:
        title = title[:pos]
    return title.decode('utf-8') #return unicode
    
def letv_download(url):
    s1 = get_html(url)
    p1 = r'''<div[^<>]*?id=.?j-videoplay.*?<script>.*?{\s*v:[[]["']([^\s]+?)["']'''
    o1 = re.search(p1,s1,re.I|re.S)
    url1 = o1.group(1) #http://g3.letv.cn/4/34/89/204323373.0.flv?b=269&tag=ios&np=1&vtype=m3u8
    url1 = base64.b64decode(url1)
    prefix = 'http://g3.letv.cn/'
    url1 = url1.replace(prefix,'',1)
    pos1 = url1.find('?')
    url1 = url1[:pos1]
    url2 = prefix + 'vod/v1/' + base64.b64encode(url1) +\
        '?format=1&b=269&expect=3&host=www_letv_com'
    #http://g3.letv.cn/vod/v1/NC8zNC84OS8yMDQzMjMzNzMuMC5mbHY=?format=1&b=269&expect=3&host=www_letv_com
    o2 = json.loads(get_html(url2))
    baseurl = o2['nodelist'][0]['location']
    urls = [] 
    new_url = baseurl + '&begin=0' + '&cLoadID=-1'
    urls.append(new_url)
    title = get_title(s1)
    download_urls(urls,title,'flv',total_size=None)


download = letv_download
download_playlist = playlist_not_supported('letv')

def main():
    script_main('letv',letv_download)

if __name__ == '__main__':
    main()

