#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
主要处理翻译中文---> 越语
'''

import re,random,md5,urllib,httplib,json
import MySQLdb,sys

#文本切割
def cut_text(text,size):
    list=[];
    total=len(text);
    if total<size:
        list.append(text)
        return list
    else:
        for i in range(0,total,size):
            item= text[i:i+size]
            list.append(item)
    return list;

#百度api
def TranslateByBaidu(text,fromLang = 'auto',toLang = 'zh'):
    appid="20180417000147511"
    secretKey="HlnWPKtXeGjHnmtpyhXK"
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = text
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
        data = json.loads(result)
        return data["trans_result"][0]["dst"]
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

if __name__=='__main__':
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    #链接数据库
    db = MySQLdb.connect(host='127.0.0.1', user="root", passwd="", db="ssh2",charset='utf8')
    # 获取操作游标
    cursor = db.cursor()
    cursor.execute("select id,title,content from news where isTranslate=0")#获得未翻译的项目
    #获得所有的结果集
    list=cursor.fetchall();
    try:
        #遍历结果集
        for item in list:
            id=str(item[0])
            title=item[1]#标题
            content=item[2]#内容
           # print "html当前中文内容：",content

            compiles = re.compile(r'<[^>]+>', re.S)
            content = compiles.sub('', content)
            # print "去除标签翻译后：",content
            content=re.sub('[\r\n\f]{2,}','\n',content);
            #print "无空格",content

            print "id--",id
            print "-----------------------------"
            content="".join(content.split()).replace("《","").replace("》","").replace("·","");
            print content
            print "-----------------------------"

            content=content.replace("（","").replace("）","").replace("•","").replace("《","").replace("》","").replace("——","").replace("(","").replace(")","").replace("—","").lower().replace("/","").replace("-","").replace("；","");
            # content=re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),content)
            content=content[0:1000]
            print "最终需要翻译的：",content
            #获得内容
            VietnameseContent=TranslateByBaidu(content.encode("utf8"), fromLang='zh',toLang='vie')
            print "翻译后的内容：",VietnameseContent
            if VietnameseContent ==None:#翻译失败
                VietnameseContent=''
            VietnameseContent=VietnameseContent.replace("'","")
            sql="update news set isTranslate=1,VietnameseContent='"+str(VietnameseContent).encode("utf8")+"'where id="+id;
            print "sql--->",sql
            print "内容执行sql结果：",cursor.execute(sql);
            db.commit()
            print "-----------------------------------"

            #获得title的翻译
            translateTitle=TranslateByBaidu(str(title), toLang='vie')
            print translateTitle
            translateTitle=translateTitle.replace("'","")
            #判断标题
            if translateTitle==None:
                translateTitle=''
            sql="update news set vietnameseTitle='"+str(translateTitle).encode("utf8")+"'where id="+id;
            print "sql--->",sql
            print "标题执行sql结果：",cursor.execute(sql);
            db.commit()
            print "-----------------------------------"
    except Exception,e:
        print "异常退出"
    finally:
        cursor.close();


