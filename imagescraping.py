# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:07:55 2019

@author: Hemanshu Namdeo
"""
import os
from bs4 import BeautifulSoup
import requests
import urllib
import re

def imgscrape(links):
    for link in links:
        url=link
        html=requests.get(url).text
        soup=BeautifulSoup(html,'lxml')
        art=soup.find('ul',class_='product__listing product__grid')
        print(url)
        for a1 in art.findAll('li'):
            name_dir=a1.span.text[:a1.span.text.find(' ')+a1.span.text[a1.span.text.find(' ')+1:].find(' ')+1]
            name_dir=name_dir.replace("/"," ")
            name_dir=name_dir.replace(" ","_")
            directory='C:\\Users\\Hemanshu Namdeo\\Desktop\\google-images-download-master\\google_images_download\\downloads\\scrapeimage\\Brands'
            if not os.path.exists(directory):
                os.makedirs(directory)
            else:   
                print(directory)
                if name_dir not in dir_name:
    #                if not os.path.exists(directory):
    #                    print('Creating Directory : ' + directory)
    #                    os.makedirs(directory)
                    dir_name[name_dir]=0
                else:        
                    dir_name[name_dir]+=1
    #            print(dir_name.keys())
                urllib.request.urlretrieve('https://www.neweracap.com%s' %(a1.img['src']),"C:\\Users\\Arun Ranganathan\\Desktop\\google-images-download-master\\google_images_download\\downloads\\scrapeimage\\Brands\\%s_%d.jpg" % (name_dir,dir_name[name_dir]))
def getlinks():
    for i in range(0,1231):
        link='https://www.neweracap.com/All-Headwear/c/AHE?q=%3Arelevance&page='+str(i)+'&scroll=toListing'
        links.append(link)

if __name__ == "__main__":
    links=[]
    dir_name={}
    getlinks()
    imgscrape(links)