#!/usr/bin/env python

__all__ = ['letv_download']

from common import *
import re,base64,json

#http://www.letv.com/ptv/pplay/5938/1.html

def letv_download(url):
    s1 = get_html(url)
    o1 = re.search(r'''<div[^<>]*?id=.?j-videoplay.*?<script>.*?{\s*v:[[]["']([^\s]+?)["']''',s1,re.I|re.S)
    url1 = o1.group(1)#http://g3.letv.cn/4/34/89/204323373.0.flv?b=269&tag=ios&np=1&vtype=m3u8
    url1 = base64.b64decode(url1)
    #http://g3.letv.cn/vod/v1/NC8zNC84OS8yMDQzMjMzNzMuMC5mbHY=?format=1&b=269&expect=3&host=www_letv_com
    prefix = 'http://g3.letv.cn/'
    url1 = url1.replace(prefix,'',1)
    pos1 = url1.find('?')
    url1 = url1[:pos1]
    url2 = prefix + 'vod/v1/' + base64.b64encode(url1) + '?format=1&b=269&expect=3&host=www_letv_com'
    o2 = json.loads(get_html(url2))
    baseurl = o2['nodelist'][0]['location']
    urls = [] 
    curr_pos = 0
    for i,each in enumerate(o2['nodelist']):
        new_url = baseurl + '&begin=' + str(curr_pos) + '&stop=' + str(curr_pos + each['gone']) + '&cLoadID=' + str(i+1)
        curr_pos += each['gone']
        urls.append(new_url)
    for each in  urls:
        print each
    title = 'test'
    download_urls(urls,title,'flv',total_size=None)


download = letv_download
download_playlist = playlist_not_supported('letv')

def main():
    script_main('letv',letv_download)

if __name__ == '__main__':
    main()

