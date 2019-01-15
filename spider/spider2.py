from bs4 import BeautifulSoup
import requests
import re
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'cookie':'clientac=1540206888578893460; visit_dt=2018-9-22; UM_distinctid=1669b7c243f27c-0ee84422e37c8b-3c604504-1fa400-1669b7c244022f; Hm_lvt_f954228be9b5d93a74a625d18203e150=1540341577; XYWYDATAxywy=1540215451-1855960778@154021545184118234963121@2; city=%C9%CF%BA%A3%CA%D0; __gg_t_city=%C9%CF%BA%A3%CA%D0; __gg_t_loc=%C9%CF%BA%A3%CA%D0; city_xywy_ad=ä¸æµ·å¸; __gg_city=ä¸æµ·å¸; beijing=false; ajsDataSession_js_test=15409026374319021197@1@1540902637@1@http%253A%252F%252Fjib.xywy.com%252Fil_sii%252Ftreat%252F597.htm@; tj_lastUrl_js_test=http%3A//jib.xywy.com/il_sii/treat/597.htm; tj_lastUrl_js_test_time=1540902637434; countNum=3; __guid=36948203.2174161411144918800.1540902652476.02; CNZZDATA30042012=cnzz_eid%3D686374698-1540899683-http%253A%252F%252Fwww.xywy.com%252F%26ntime%3D1540899683; ajsDataSession=15409026366751111876@4@1540902664@1@http%253A%252F%252Fzzk.xywy.com%252F4516_gaishu.html@http%253A%252F%252Fzzk.xywy.com%252F%253Ffromurl%253Dxywyhomepage; tj_lastUrl=http%3A//zzk.xywy.com/4516_gaishu.html; tj_lastUrl_time=1540902664717; monitor_count=3'
}
BASE_PATH='http://zzk.xywy.com/p/'
def gethtml(url):
    req=requests.get(url,headers=headers)
    html=req.content
    return html
def parse_sysptom(html,htmlstr):
    soup=BeautifulSoup(htmlstr,'lxml')
    #print(soup)
    datalist=soup.find_all('ul',
                           {'class':'ks-ill-list clearfix mt10'})
    descriptionlist=[]
    urllist=[]
    for i,data in enumerate(datalist):

        pattern1 = '<a.*?title="(.+)".*?>(.*?)</a>'
        ret = re.search(pattern1,str(data))
        for x in ret.groups():
            descriptionlist.append(x)
        pattern2 = '<a.*?href="(.+)".*?>(.*?)</a>'
        ret = re.search(pattern2,str(data))
        for x in ret.groups():
            url=x.split(' ')[0].replace('"','')
            urllist.append(html+url)
            break
    for description,url in zip(descriptionlist,urllist):
        diseaselist=parse_possible_disease(url)
        print(description)
        print(diseaselist)
def parse_possible_disease(url):
    html_doc=gethtml(url)
    soup=BeautifulSoup(html_doc,'lxml')
    datalist=soup.find_all('li',{
        'class':'loop-tag-name mr20'
    })
    diseaselist=[]
    for i,data in enumerate(datalist):
        dr = re.compile(r'<[^>]+>',re.S)
        data = dr.sub('',str(data))
        if(i!=0):
            diseaselist.append(data)
    return diseaselist
html_doc=gethtml('http://zzk.xywy.com/p/xiaohuaneike.html')
parse_sysptom('http://zzk.xywy.com',html_doc)