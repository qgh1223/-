import re

import requests
from bs4 import BeautifulSoup

from ask1.dbopt.neoaddopt import NeoRelationOpt

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'cookie':'BAIDUID=D7D986999EA2CD4E68B321058FA00EFA:FG=1; PSTM=1537543374; BIDUPSID=D36E28D2FFACE7BAD39578428ABDC97A; locale=zh; cflag=15%3A3; BDUSS=zFtWXNZVlp0VjRNdWpIZlhtOWtJRTltTTFtLTE0NGJHa0lubmExYmV6QlUtZU5iQVFBQUFBJCQAAAAAAAAAAAEAAAAolghZcWdoMTIyMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFRsvFtUbLxbZ; pgv_pvi=3620062208'
}
component=['cause','prevent','neopathy',
           'symptom','inspect','diagnosis',
           'treat','nursing','food']
def gethtml(url):
    req=requests.get(url,headers=headers)
    html=req.content
    return html
def parse_introduction(htmlstr,disease):
    soup=BeautifulSoup(htmlstr)
    datalist=soup.find_all('p',
                           {'class':'clearfix'})
    for data in datalist:
        data=str(data)
        data=data.replace('<p class="clearfix">','')
        data=data.replace('</p>','')
        data=data.replace('<!-- -->','')
        data=data.replace('<span class="fr common-right">','')
        data=data.replace('\n','')
        dr = re.compile(r'<[^>]+>',re.S)
        data = dr.sub('',data)
        data=data.replace('&gt;','')
        datalist=data.split('：')
        print(datalist)
        NeoRelationOpt(disease,datalist[0],datalist[1]).add_opt()
def parse_html(htmlstr):
    soup=BeautifulSoup(htmlstr,'lxml')
    print(soup)

def parse_disease_num(html,htmlstr):
    soup=BeautifulSoup(htmlstr,'lxml')
    datalist=soup.find_all('ul',
                           {'class':'ks-ill-list clearfix mt10'})
    print(len(datalist))
    hrefset=set()
    diseaseset=set()
    for i,data in enumerate(datalist):
        pattern = '<a.*?href="(.+)".*?>(.*?)</a>'
        ret = re.search(pattern,str(data))
        href1=''
        for j,x in enumerate(ret.groups()):
            #print(x)
            x1=x.split('"')[0]
            x2=x.split('"')[-1]
            #print(x1)
            #print(x1[0])
            if(x1[0]=='/'):

                href1=html+x1
                hrefset.add(href1)
            elif(x1[0]!='h'):

                diseasename=x1
                diseaseset.add(diseasename)
        if(i>20):
            break
    for (href,diseasename) in zip(hrefset,diseaseset):
        html_doc=gethtml(href)
        parse_introduction(html_doc,diseasename)
    print(diseaseset)
    print(hrefset)
#html_doc=gethtml('http://jib.xywy.com/html/neike.html')
kindlist=['neike','huxineike','xiaohuaneike','miniaoneike','xinneike','xueyeke','shenneike']
html_doc=gethtml('http://jib.xywy.com/html/xiaohuaneike.html')
parse_disease_num('http://jib.xywy.com',html_doc)
