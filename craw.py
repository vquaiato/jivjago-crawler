import sys
import urllib2
import re
import os.path
import time
import threading
from threading import Thread

base_url = "http://www.jivjago.com/audio/"
processed = []
downloaded = 0

def read(url):
    u = urllib2.urlopen(url)
    contents = u.read()
    return contents

def read_music_links(current_url):
    contents = read(current_url)
    links = re.findall('href="(.{2,1000})"', contents)
    mp3_links = []
    for link in links:
        if re.search("(\..{3})$", link, re.I):
            mp3_links.append(current_url + link)
        else:
            if (not (link in processed)) and (not re.search(link, current_url)):
                print "> " + current_url + link
                processed.append(current_url + link)
                mp3_links += read_music_links(current_url + link)
    return mp3_links

def download_files(mp3_links):
    allowed_threads = 15
    for mp3 in mp3_links:
        while(threading.activeCount() > allowed_threads):
            time.sleep(20)
        th = Thread(target=download_file, args=(mp3,))
        th.start()

def download_file(mp3):
    print "downloading > " + mp3
    file_name = mp3.split("/")[-1]
    if not os.path.isfile(file_name):
        global downloaded
        downloaded=downloaded+1
        print downloaded
        u = urllib2.urlopen(mp3.replace("&amp;", "&"))
        # tries = 1
        # while os.path.isfile(file_name):
        #     file_name = '[%d]_%s' % (tries, file_name)
        #     tries = tries + 1

        localFile = open(file_name, 'w')
        localFile.write(u.read())
        localFile.close()

def start():
    processed.append("/audio/")
    mp3_links = read_music_links(base_url)
    download_files(mp3_links)

start()
