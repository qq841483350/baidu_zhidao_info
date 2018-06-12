#coding:utf8
#百度知道问答内容抓取
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests,re,os,time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers={

    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
}
def get_html(url):
    while 1:
        try:
            r=requests.get(url,verify=False)
            r.encoding="gbk"
            html=r.text
            return html
        except:
            pass

def get_info(url):
    html=get_html(url)
    urls=re.findall('<a href="(.*?)\?fr=iks',html)
    for url in urls:
        if 'zhidao' in url:
            html=get_html(url)
            if '发布于' in html:
                title=re.findall(u'<title>([\s\S]*?)_百度知道</title>',html)[0]
                #content=re.findall('<div class="line content">([\s\S]*?)<div id="show-answer-hide">',html)[0]
                content=re.findall('<div class="line content">([\s\S]*?)iknow-qb_home_icons',html)[0]
                content=re.sub(u'本回答由[\s\S]*?推荐</div>','',content)
                content=re.sub(u'评论','',content)
                content=re.sub(u'本回答被提问者采纳','',content)
                content=re.sub(u'其他回答','',content)
                content=re.sub(u'追问','',content)
                content=re.sub(u'热心网友','',content)
                content=re.sub(u'答案纠错','',content)
                #content=re.sub('<p class="mb-5">[\s\S]*?</p>\s+</div>','',content)
                content=re.sub('<script[\s\S]*?</script>','',content)
                content=re.sub('<span class="pos-time">[\s\S]*?</span>\s+</div>','',content)
                content=re.sub('<a alog-action="qb-username[\s\S]*?</a>\s+</div>','',content)
                content=re.sub('<span class="f-pipe">[\s\S]*?</span>\s+<div class="grid-r f-aid pos-relative">','',content)
                content=re.sub('<a alog-action="qb-username[\s\S]*?</a>\s+<span class="i-gradeIndex i-gradeIndex-\d+">','',content)
                content=re.sub('<[\s\S]*?>','',content)
                content=re.sub('\s+','',content)
                content=re.sub('</[\s\S]*?>','',content)
                content=re.sub('<iclass="','',content)
                content=re.sub('\|','',content)
                content=re.sub('"class="ikqb_img_alink"','',content)

                print '标题:',title+"\n"+"\n",'回答：',content+"\n"+"\n"

            else:
                pass
        else:
            pass



if __name__=="__main__":
    print '''《百度知道问答内容抓取》

1、软件开发者：李亚涛

2、个人微信：841483350

3、微信公众号：qq841483350,欢迎关注

4、使用方法：在下方输入一个关键词，然后按 回车 继续即可
'''

    keyword=raw_input('请输入一个关键词,然后按 回车 继续:')
    url1="https://zhidao.baidu.com/search?pn=0&word=%s"%keyword
    # print url1
    html1=get_html(url1)
    id1=re.findall(u'<span class="f-lighter lh-22">共(.*?)条结果</span>',html1)[0]
    id1=re.sub(',','',id1)
    id2=int(id1)/10

    if id2>=75:
        for id in range(0,77): #共76页
            num=id*10

            url="http://zhidao.baidu.com/search?pn=%s&word=%s"%(num,keyword)
            # print '正在挖掘',url,'第',id+1,'页的关键词'
            print '【【【【【正在挖掘第',id+1,'页的问答】】】】】'+"\n"+"\n"
            time.sleep(1)
            get_info(url)

    elif 1<id2<75:

        for id in range(0,id2): #共76页
        # for id in range(0,77): #共76页
            num=id*10

            url="https://zhidao.baidu.com/search?pn=%s&word=%s"%(num,keyword)
            # print '正在挖掘',url,'第',id+1,'页的关键词'
            print '【【【【【正在挖掘第',id+1,'页的问答】】】】】'+"\n"+"\n"
            time.sleep(1)
            get_info(url)

    else:
        print '信息量太少'

