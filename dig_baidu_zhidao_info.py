#coding:utf8
#百度知道问答内容抓取，标题与回答抓取并自动导出到文本文档
import sys,wx,lxml.html,requests,threading
reload(sys)
sys.setdefaultencoding('utf-8')
import requests,re,os,time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"}
def get_html(url):
    while 1:
        try:
            r=requests.get(url,verify=False)
            r.encoding="gbk"
            html=r.text
            return html
        except:
            pass
list=[]
def get_word(keyword):
    # content2.Clear()
    # keyword=content1.GetValue()
    # keyword=str(keyword).strip()
    # keyword=raw_input('请输入一个关键词,然后按 回车 继续:')
    url1="https://zhidao.baidu.com/search?pn=0&word=%s"%keyword
    get_info(url1)#第一页问答采集
    get_next_page_url(url1)


def get_next_page_url(url):
    html1=get_html(url)
    selector=lxml.html.fromstring(html1)
    # https://zhidao.baidu.com/search?word=%B7%BF%B2%FA&ie=gbk&site=-1&sites=0&date=0&pn=10
    next_page=selector.xpath('//a[@class="pager-next"]/@href')
    if next_page:
        next_page_url="https://zhidao.baidu.com"+next_page[0]
        get_info(next_page_url) #下一页问答信息采集
        get_next_page_url(next_page_url)

    else:
        print '关键词'.decode('utf8'),keyword,'信息抓取完毕'.decode('utf8')


def get_info(url):
    html=get_html(url)
    urls=re.findall('<a href="(.*?)\?fr=iks',html)
    for url in urls:
        # info_append(url)
        x=threading.Thread(target=info_append,args=(url,))
        x.start()

def info_append(url):
    # global keyword1
    # keyword1="word"
    if 'zhidao' in url:
        html=get_html(url)
        if '发布于' in html:
            title=re.findall(u'<title>([\s\S]*?)_百度知道</title>',html)[0]
            #content=re.findall('<div class="line content">([\s\S]*?)<div id="show-answer-hide">',html)[0]
            content=re.findall('<div class="line content">([\s\S]*?)iknow-qb_home_icons',html)
            if content:
                content=content[0]
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

                result=title+"\n\n"+content+"\n"+"\n"
                print result
                f=open('%s.txt'%keyword.decode('utf8').encode('gbk'),'a')
                f.write(result)
                f.close()
                print result
            else:
                pass

            # time.sleep(1)
            # content2.AppendText(result)
            # print '标题:',title+"\n"+"\n",'回答：'+content+"\n"+"\n"

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

'''.decode('utf8')
    while True:

        keyword=raw_input("enter the keyword:")
        get_word(keyword)
        os.system('%s.txt'%keyword.decode('utf8'))
        # raw_input("continue:")


    # app=wx.App()
    # win=wx.Frame(None,title="【百度知道信息抓取】使用方法：填入接口地址与URL然后点击提交运行 《开发者:李亚涛,微信:841483350》".decode('utf8'),size=(850,700))
    # icon=wx.Icon('favicon.ico',wx.BITMAP_TYPE_ICO)
    # win.SetIcon(icon)
    # win.Show()
    # wx.StaticText(win,label="*接口调用地址:",pos=(100,12),size=(80,30))
    # # content1=wx.TextCtrl(win,pos=(185,5),size=(500,30),style = wx.TE_MULTILINE | wx.TE_RICH)
    # content1=wx.TextCtrl(win,pos=(185,5),size=(500,30))
    #
    # wx.StaticText(win,label="*请在下方填入需要提交的URL地址，一行一个,然后点击提交",pos=(100,40),size=(500,30))
    # content2=wx.TextCtrl(win,pos=(100,70),size=(640,550),style=wx.TE_MULTILINE|wx.TE_RICH)
    # loadButton=wx.Button(win,label='提交'.decode('utf8'),pos=(690,5),size=(50,30))
    # loadButton.Bind(wx.EVT_BUTTON,get_word)  #这个按钮绑定xiongzhang这个函数
    #
    # app.MainLoop()


