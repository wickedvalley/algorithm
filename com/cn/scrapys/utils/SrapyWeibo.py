#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
爬取微博信息
'''
import sys
import time
import json
import csv
import codecs
import requests
from bs4 import BeautifulSoup

class ScrapyWeibo():

    def __init__(self):
        # 设置页面编码
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')
        self.url='https://s.weibo.com/weibo/%25E8%259A%2582%25E8%259A%2581%25E6%25A3%25AE%25E6%259E%2597&Refer=STopic_box'
        self.session=requests.session();
        self.count=0;#爬取的数量

        #写入csv相关
        self.csvfile = file('D:\\weibo_result.csv', 'wb')
        self.csvfile.write(codecs.BOM_UTF8)
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(['微博', '发送人', '发送时间','转发数','评论数','点赞数','评论','评论的回复','微博图片']) #存储8列数据


    def writeImg(self,url):
        # 这是一个图片的url
        # url = 'http://ww4.sinaimg.cn/square/6a7775d5gy1frd6ctuk91j20v90kutfh.jpg'
        response = requests.get("http:"+url)
        # 获取的文本实际上是图片的二进制文本
        img = response.content
        print "下载图片：",url
        fileName=url.split("/")[-1]
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        with open('D:\\imgs\\'+fileName, 'wb') as f:
            f.write(img)

    def job(self,url):
        headers={
            'Host':'s.weibo.com',
            'Referer':'https://s.weibo.com/weibo/%25E8%259A%2582%25E8%259A%2581%25E6%25A3%25AE%25E6%259E%2597?topnav=1&wvr=6&b=1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        session=self.session
        response=session.get(url,headers=headers)
        lines=response.text.splitlines()
        millis = int(round(time.time() * 1000)) #时间戳
        for line in lines:
            ## 判断是否有微博内容，出现这一行，则说明没有被认为是机器人
            if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
                isCaught = False
                n = line.find('html":"')
                if n > 0:
                    j = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\","")  # 去掉所有的\
                    ## 没有更多结果页面
                    if (j.find('<div class="search_noresult">') > 0):
                        hasMore = False
                        ## 有结果的页面
                    else:

                        bs = BeautifulSoup(j.decode('utf-8'), "html.parser")

                        contents=bs.find_all(attrs={'class': 'content clearfix'})

                        items = bs.find_all(attrs={'action-type': 'feed_list_item'})

                        index=-1;
                        for item in contents:
                            index+=1
                            nickName = item.find('a').get("nick-name")  # 发微博人
                            nickUrl = item.find('a').get("href")  # 链接
                            content = str(item.find('p').getText()).strip()  # 发布内容
                            publishTime = item.find(attrs={'class', 'feed_from W_textb'}).a.get('title')  # 发布时间
                            dispathCount = 0;  # 转发数
                            commentsCount = 0;  # 评论数
                            startCount = 0;  # 点赞数
                            topComment = ''  # 评论
                            topReply = ''  # 评论的回复

                            try:
                                for img in item.find(attrs={'class','WB_media_a WB_media_a_mn clearfix'}).find_all('img'):
                                    print "有图片链接",img.get('src')
                                    self.writeImg(str(img.get('src')).strip())

                            except Exception,e:
                                print "没有图片"

                            print "昵称：",item.find('a').get("nick-name")
                            print "链接：",item.find('a').get("href")
                            print "内容：",str(item.find('p').getText()).strip()
                            print "发布时间：",item.find(attrs={'class','feed_from W_textb'}).a.get('title')
                            commentList=items[index].find(attrs={'class','feed_action clearfix'}).find_all('em')
                            nums=len(commentList)
                            commentsNum=0;#评论数
                            if int(nums) == 3:
                                commentsNum = commentList[1].getText()
                                print "转发：", commentList[0].getText()
                                print "评论：", commentList[1].getText()
                                print "点赞：", commentList[2].getText()
                                dispathCount = commentList[0].getText()
                                commentsCount = commentList[1].getText()
                                startCount = commentList[2].getText()
                            else:
                                commentsNum = commentList[0].getText()
                                print "转发：", 0
                                print "评论：", commentList[0].getText()
                                print "点赞：", commentList[1].getText()
                                dispathCount = 0
                                commentsCount = commentList[0].getText()
                                startCount = commentList[1].getText()

                            mid=items[index].get('mid')
                            print "mid:",mid

                            if str(commentsNum) not in '':
                                if int(commentsNum)>0 and int(commentsNum)>30:#有评论，获取评论
                                    print "有评论：",commentsNum

                                    try:
                                        headers['Cookie']='SINAGLOBAL=6173626529602.904.1526178661648; un=13349832221; wvr=6; UOR=www.baidu.com,s.weibo.com,www.baidu.com; ALF=1557992269; SSOLoginState=1526456270; SCF=AqR6l56W-ZKWmWtwiLa8ZipKOr8rFZsbGbAEYhm_qaC_DgMd8HGfk_kEGuiUB1ajfvKwv2-Azyav1ZHbLiLBt-0.; SUB=_2A253_6-eDeRhGeNP6FUQ8CnEwz6IHXVUjIZWrDV8PUNbmtBeLWz-kW9NToQaNo1H3da86GwUcsarp2R895BqVVkn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52Kk6PuTm9aYlsesVoQ_Rb5JpX5KzhUgL.Fo-pe0MpehMR1hz2dJLoIEBLxKBLB.eL122LxKqL1K.LBKnLxKqL1--LB-zLxK-LBo5L1K2t; SUHB=0KABMewgFQvQmz; _s_tentry=login.sina.com.cn; Apache=2741538761998.934.1526456266005; ULV=1526456266052:3:3:3:2741538761998.934.1526456266005:1526372677841; SWBSSL=usrmdinst_6; SWB=usrmdinst_15; WBStorage=5548c0baa42e6f3d|undefined'
                                        url='https://s.weibo.com/ajax/comment/small?act=list&mid='+str(mid)+'&uid=5137107882&smartFlag=false&smartCardComment=&isMain=true&suda-data=key%253Dtblog_search_weibo%2526value%253Dweibo_ss_page_p_p&pageid=weibo&_t=0&__rnd='+str(millis)
                                        response=session.get(url=url,headers=headers)
                                        print "---------获取评论urlMore-----------"
                                        response=json.loads(response.text)['data']['html']
                                        bs = BeautifulSoup(response, "html.parser")
                                        urlMore='https:'+bs.find(attrs={'class','WB_cardmore S_txt1 S_line1 clearfix'}).get('href')+'&type=comment'
                                        print "点击更多：",urlMore


                                        #获得所有的平路
                                        url='https://weibo.com/aj/v6/comment/big?ajwvr=6&id='+str(mid)+'&from=singleWeiBo&__rnd='+str(millis)
                                        headers['Referer']=urlMore
                                        headers['Host']='weibo.com'
                                        headers['Cookie']='SINAGLOBAL=6173626529602.904.1526178661648; un=13349832221; wvr=6; UOR=www.baidu.com,s.weibo.com,www.baidu.com; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; ALF=1557992269; SSOLoginState=1526456270; SCF=AqR6l56W-ZKWmWtwiLa8ZipKOr8rFZsbGbAEYhm_qaC_DgMd8HGfk_kEGuiUB1ajfvKwv2-Azyav1ZHbLiLBt-0.; SUB=_2A253_6-eDeRhGeNP6FUQ8CnEwz6IHXVUjIZWrDV8PUNbmtBeLWz-kW9NToQaNo1H3da86GwUcsarp2R895BqVVkn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52Kk6PuTm9aYlsesVoQ_Rb5JpX5KzhUgL.Fo-pe0MpehMR1hz2dJLoIEBLxKBLB.eL122LxKqL1K.LBKnLxKqL1--LB-zLxK-LBo5L1K2t; SUHB=0KABMewgFQvQmz; YF-V5-G0=4955da6a9f369238c2a1bc4f70789871; _s_tentry=login.sina.com.cn; Apache=2741538761998.934.1526456266005; ULV=1526456266052:3:3:3:2741538761998.934.1526456266005:1526372677841; YF-Page-G0=d52660735d1ea4ed313e0beb68c05fc5; TC-V5-G0=7975b0b5ccf92b43930889e90d938495'
                                        response=session.get(url=url,headers=headers,allow_redirects=False)
                                        print "---------获取评论列表-----------"
                                        response=json.loads(response.text)['data']['html']
                                        bs = BeautifulSoup(response, "html.parser")
                                        commentItems=bs.find_all(attrs={'class','list_li S_line1 clearfix'})
                                        for one in commentItems:
                                            print one.find(attrs={'class','WB_text'})
                                            print "评论人：",str(one.find(attrs={'class','WB_text'}).getText()).split("：")[0].strip()
                                            print "评论内容：",str(one.find(attrs={'class','WB_text'}).getText()).split("：")[1].strip()
                                            print "时间：",one.find(attrs={'class','WB_from S_txt2'}).getText()
                                            print "点赞数：",str(one.find(attrs={'class','WB_handle W_fr'}).find_all('a')[-1].find_all('em')[-1].getText()).replace('赞','0')

                                            # 评论内容
                                            topComment = str(one.find(attrs={'class', 'WB_text'}).getText()).split("：")[
                                                1].strip()

                                            reply = one.find(attrs={'class', 'list_box_in S_bg3'}).find(
                                                attrs={'class', 'WB_text'}).getText()
                                            replyPerson = str(reply).split("：")[0].strip()
                                            replyContent = str(reply).split("：")[1].strip()
                                            print '----有回复----', reply
                                            print "回复人：", replyPerson
                                            print "回复内容：", replyContent

                                            topReply = replyContent
                                            self.writer.writerow(
                                                [content, nickName, publishTime, dispathCount, commentsCount,
                                                 startCount, topComment, ''])  # 存储8列数据
                                    except Exception,e:
                                        print "异常：",e.message

                            print
                            print


    def work(self):
        session = self.session
        url='https://s.weibo.com/weibo/%25E8%259A%2582%25E8%259A%2581%25E6%25A3%25AE%25E6%259E%2597&page='
        for i in range(2,50):
            time.sleep(3)
            url+=str(i)
            print "当前页码：",i

            headers = {
                'Cookie':'SINAGLOBAL=6173626529602.904.1526178661648; un=13349832221; wvr=6; UOR=www.baidu.com,s.weibo.com,www.baidu.com; SSOLoginState=1526456270; _s_tentry=login.sina.com.cn; Apache=2741538761998.934.1526456266005; ULV=1526456266052:3:3:3:2741538761998.934.1526456266005:1526372677841; SWBSSL=usrmdinst_6; SWB=usrmdinst_15; WBtopGlobal_register_version=3ae140abebd3cc86; un=13349832221; ULOGIN_IMG=15265646429657; login_sid_t=23733e2131056b02e3a38140f44bfdc1; cross_origin_proto=SSL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52Kk6PuTm9aYlsesVoQ_Rb5JpX5K2hUgL.Fo-pe0MpehMR1hz2dJLoIEBLxKBLB.eL122LxKqL1K.LBKnLxKqL1--LB-zLxK-LBo5L1K2t; ALF=1558191982; SCF=AqR6l56W-ZKWmWtwiLa8ZipKOr8rFZsbGbAEYhm_qaC_NcqKuWa_VwB5cqFW62E0Z6CYOvfh3QKuq7RYkNZTQ6U.; SUB=_2A253-pujDeRhGeNP6FUQ8CnEwz6IHXVVcYprrDV8PUNbmtANLXPNkW9NToQaNg2QcrSg2TTijJDXnNMhSlB_9HlI; SUHB=0tKa7qzbZp6g9e; WBStorage=5548c0baa42e6f3d|undefined',
                'Host': 's.weibo.com',
                'Referer': 'https://s.weibo.com/weibo/%25E8%259A%2582%25E8%259A%2581%25E6%25A3%25AE%25E6%259E%2597&Refer=STopic_box',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
            }
            response = session.get(url, headers=headers,allow_redirects=False)
            lines = response.text.splitlines()
            millis = int(round(time.time() * 1000))  # 时间戳
            for line in lines:
                # time.sleep(3)
                ## 判断是否有微博内容，出现这一行，则说明没有被认为是机器人
                if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
                    isCaught = False
                    n = line.find('html":"')
                    if n > 0:
                        j = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\",
                                                                                                              "")  # 去掉所有的\
                        ## 没有更多结果页面
                        if (j.find('<div class="search_noresult">') > 0):
                            hasMore = False
                            ## 有结果的页面
                        else:

                            bs = BeautifulSoup(j.decode('utf-8'), "html.parser")

                            contents = bs.find_all(attrs={'class': 'content clearfix'})

                            items = bs.find_all(attrs={'action-type': 'feed_list_item'})

                            index = -1;
                            for item in contents:
                                flag=False      #标示是否有评论
                                index += 1
                                nickName=item.find('a').get("nick-name")                                    #发微博人
                                nickUrl=item.find('a').get("href")                                          #链接
                                content=str(item.find('p').getText()).strip()                               #发布内容
                                publishTime=item.find(attrs={'class', 'feed_from W_textb'}).a.get('title')  #发布时间
                                dispathCount=0;                                                             #转发数
                                commentsCount=0;                                                            #评论数
                                startCount=0;                                                               #点赞数
                                topComment=''                                                               #评论
                                topReply=''                                                                 #评论的回复
                                imgUrls=''                                                                  #微博图片

                                #处理图片的下载
                                try:
                                    for img in item.find(attrs={'class', 'WB_media_a WB_media_a_mn clearfix'}).find_all(
                                            'img'):
                                        print "有图片链接", img.get('src')
                                        imgUrl=str(img.get('src')).strip()
                                        self.writeImg(imgUrl)
                                        fileName = imgUrl.split("/")[-1]
                                        imgUrls+=fileName+","

                                except Exception, e:
                                    print "没有图片"

                                print "昵称：", item.find('a').get("nick-name")
                                print "链接：", item.find('a').get("href")
                                print "内容：", str(item.find('p').getText()).strip()
                                print "发布时间：", item.find(attrs={'class', 'feed_from W_textb'}).a.get('title')
                                commentList = items[index].find(attrs={'class', 'feed_action clearfix'}).find_all('em')
                                nums = len(commentList)
                                commentsNum = 0;  # 评论数
                                if int(nums) == 3:
                                    commentsNum = commentList[1].getText()
                                    print "转发：", commentList[0].getText()
                                    print "评论：", commentList[1].getText()
                                    print "点赞：", commentList[2].getText()
                                    dispathCount=commentList[0].getText()
                                    commentsCount=commentList[1].getText()
                                    startCount=commentList[2].getText()
                                else:
                                    commentsNum = commentList[0].getText()
                                    print "转发：", 0
                                    print "评论：", commentList[0].getText()
                                    print "点赞：", commentList[1].getText()
                                    dispathCount=0
                                    commentsCount=commentList[0].getText()
                                    startCount=commentList[1].getText()

                                mid = items[index].get('mid')
                                print "mid:", mid

                                if str(commentsNum) not in '':
                                    if int(commentsNum) > 0 and int(commentsNum) > 0:  # 有评论，获取评论
                                        print "有评论：", commentsNum
                                        try:
                                            headers[
                                                'Cookie'] = 'SINAGLOBAL=6173626529602.904.1526178661648; un=13349832221; wvr=6; UOR=www.baidu.com,s.weibo.com,www.baidu.com; SSOLoginState=1526456270; _s_tentry=login.sina.com.cn; Apache=2741538761998.934.1526456266005; ULV=1526456266052:3:3:3:2741538761998.934.1526456266005:1526372677841; SWBSSL=usrmdinst_6; SWB=usrmdinst_15; WBtopGlobal_register_version=3ae140abebd3cc86; un=13349832221; ULOGIN_IMG=15265646429657; login_sid_t=23733e2131056b02e3a38140f44bfdc1; cross_origin_proto=SSL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52Kk6PuTm9aYlsesVoQ_Rb5JpX5K2hUgL.Fo-pe0MpehMR1hz2dJLoIEBLxKBLB.eL122LxKqL1K.LBKnLxKqL1--LB-zLxK-LBo5L1K2t; ALF=1558191982; SCF=AqR6l56W-ZKWmWtwiLa8ZipKOr8rFZsbGbAEYhm_qaC_NcqKuWa_VwB5cqFW62E0Z6CYOvfh3QKuq7RYkNZTQ6U.; SUB=_2A253-pujDeRhGeNP6FUQ8CnEwz6IHXVVcYprrDV8PUNbmtANLXPNkW9NToQaNg2QcrSg2TTijJDXnNMhSlB_9HlI; SUHB=0tKa7qzbZp6g9e; WBStorage=5548c0baa42e6f3d|undefined'
                                            url = 'https://s.weibo.com/ajax/comment/small?act=list&mid=' + str(
                                                mid) + '&uid=5137107882&smartFlag=false&smartCardComment=&isMain=true&suda-data=key%253Dtblog_search_weibo%2526value%253Dweibo_ss_page_p_p&pageid=weibo&_t=0&__rnd=' + str(
                                                millis)
                                            response = session.get(url=url, headers=headers)
                                            print "---------获取评论urlMore-----------"
                                            response = json.loads(response.text)['data']['html']
                                            bs = BeautifulSoup(response, "html.parser")
                                            urlMore = 'https:' + bs.find(
                                                attrs={'class', 'WB_cardmore S_txt1 S_line1 clearfix'}).get(
                                                'href') + '&type=comment'
                                            print "点击更多：", urlMore

                                            # 获得所有的平路
                                            url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=' + str(
                                                mid) + '&from=singleWeiBo&__rnd=' + str(millis)
                                            headers['Referer'] = urlMore
                                            headers['Host'] = 'weibo.com'
                                            headers[
                                                'Cookie'] = 'SINAGLOBAL=6173626529602.904.1526178661648; un=13349832221; wvr=6; UOR=www.baidu.com,s.weibo.com,www.baidu.com; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; SSOLoginState=1526456270; YF-V5-G0=4955da6a9f369238c2a1bc4f70789871; _s_tentry=login.sina.com.cn; Apache=2741538761998.934.1526456266005; ULV=1526456266052:3:3:3:2741538761998.934.1526456266005:1526372677841; YF-Page-G0=d52660735d1ea4ed313e0beb68c05fc5; TC-V5-G0=7975b0b5ccf92b43930889e90d938495; TC-Page-G0=c9fb286cd873ae77f97ce98d19abfb61; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; ULOGIN_IMG=15265646429657; login_sid_t=23733e2131056b02e3a38140f44bfdc1; cross_origin_proto=SSL; WBtopGlobal_register_version=3ae140abebd3cc86; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52Kk6PuTm9aYlsesVoQ_Rb5JpX5K2hUgL.Fo-pe0MpehMR1hz2dJLoIEBLxKBLB.eL122LxKqL1K.LBKnLxKqL1--LB-zLxK-LBo5L1K2t; ALF=1558191982; SCF=AqR6l56W-ZKWmWtwiLa8ZipKOr8rFZsbGbAEYhm_qaC_NcqKuWa_VwB5cqFW62E0Z6CYOvfh3QKuq7RYkNZTQ6U.; SUB=_2A253-pujDeRhGeNP6FUQ8CnEwz6IHXVVcYprrDV8PUNbmtANLXPNkW9NToQaNg2QcrSg2TTijJDXnNMhSlB_9HlI; SUHB=0tKa7qzbZp6g9e'
                                            response = session.get(url=url, headers=headers, allow_redirects=False)
                                            print "---------获取评论列表-----------"
                                            response = json.loads(response.text)['data']['html']
                                            bs = BeautifulSoup(response, "html.parser")
                                            commentItems = bs.find_all(attrs={'class', 'list_li S_line1 clearfix'})
                                            for one in commentItems:
                                                print one.find(attrs={'class', 'WB_text'})
                                                print "评论人：", \
                                                str(one.find(attrs={'class', 'WB_text'}).getText()).split("：")[
                                                    0].strip()
                                                print "评论内容：", \
                                                str(one.find(attrs={'class', 'WB_text'}).getText()).split("：")[
                                                    1].strip()
                                                print "时间：", one.find(attrs={'class', 'WB_from S_txt2'}).getText()
                                                print "点赞数：", str(
                                                    one.find(attrs={'class', 'WB_handle W_fr'}).find_all('a')[
                                                        -1].find_all('em')[-1].getText()).replace('赞', '0')

                                                #评论内容
                                                topComment=str(one.find(attrs={'class', 'WB_text'}).getText()).split("：")[1].strip()
                                                try:
                                                    reply=one.find(attrs={'class','list_box_in S_bg3'}).find(attrs={'class', 'WB_text'}).getText()
                                                    replyPerson=str(reply).split("：")[0].strip()
                                                    replyContent=str(reply).split("：")[1].strip()
                                                    print '----有回复----',reply
                                                    print "回复人：",replyPerson
                                                    print "回复内容：",replyContent

                                                    topReply=replyContent
                                                    self.writer.writerow(
                                                        [content, nickName, publishTime, dispathCount, commentsCount,
                                                         startCount, topComment, topReply,imgUrls])  # 存储8列数据
                                                except Exception,e:
                                                    print "没有回复",e.message


                                        except Exception, e:
                                            print "异常：", e.message

                                #没有评论
                                else:
                                    print
                                    self.writer.writerow(
                                        [content,nickName, publishTime, dispathCount,commentsCount, startCount, topComment, topReply,imgUrls])  # 存储8列数据
                                url = 'https://s.weibo.com/weibo/%25E8%259A%2582%25E8%259A%2581%25E6%25A3%25AE%25E6%259E%2597&page='
                                print
                                print



if __name__=='__main__':

    obj=ScrapyWeibo();
    # obj.job(obj.url)
    obj.work()
