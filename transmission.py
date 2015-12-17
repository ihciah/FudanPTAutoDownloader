# -*- coding: utf-8 -*-
#自动判别种子并下载
import transmissionrpc, base64
import cookielib, urllib2, urllib, re, hashlib, time, json, os
from multiprocessing.dummy import Pool as ThreadPool
from judger import judge
import cPickle as pickle

class config:
    ptusername="ihciah"
    ptuserinfo=""
    save_path="/home/c/workspace/pt/seeds_auto"
    token_path="/home/c/workspace/pt/token.pkl"

class ihcteansmission:
    def __init__(self):
        self.tc = transmissionrpc.Client("your_transmission_ip",port=9091,user="username",password="password")
    def download(self,filename):
        print self.tc.add_torrent(base64.b64encode(open(filename,"rb").read()))

class torrent_checker:
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    tc=ihcteansmission()
    config=config()
    def login(self):
        if os.path.isfile(self.config.token_path):
            self.cj.load(self.config.token_path, ignore_discard=False, ignore_expires=False)
            t=self.opener.open("http://pt.vm.fudan.edu.cn/index.php").read()
            if t.find("http://pt.vm.fudan.edu.cn/index.php?action=logout")!=-1:
                print "Token loaded from file."
                return 0
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')]
        self.opener.addheaders = [('Origin', 'http://pt.vm.fudan.edu.cn')]
        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]
        self.opener.addheaders = [('Accept-Encoding', 'deflate')]
        self.opener.addheaders = [('DNT', '1')]
        self.opener.addheaders = [('Accept-Language', 'zh-CN,zh;q=0.8')]
        self.opener.addheaders = [('Host', 'pt.vm.fudan.edu.cn')]
        self.opener.addheaders = [('Referer', 'http://pt.vm.fudan.edu.cn/index.php?action=login2')]
        res=self.opener.open("http://pt.vm.fudan.edu.cn/index.php?action=login2").read()
        time.sleep(2)
        p=re.compile(r"sSessionId:'(\w*)")
        r=p.search(res)
        sessionid=r.groups()[0]
        h=hashlib.sha1()
        h.update(self.config.ptuserinfo+sessionid)
        hexd=h.hexdigest()
        userdata=urllib.urlencode({"user":self.config.ptusername,"passwrd":"","cookielength":1440,"hash_passwrd":hexd})
        t=self.opener.open("http://pt.vm.fudan.edu.cn/index.php?action=login2",userdata).read()
        if t.find("http://pt.vm.fudan.edu.cn/index.php?action=logout")!=-1:
            print "PT@platform Login Success"
            self.cj.save(self.config.token_path)
            print "Token saved."
            return 0
        else:
            print "PT@platform Login Failed"
            return -1
    def filter_func(self,t_info):
        judger=judge(t_info,self.opener)
        return judger.judge()
    def down_page(self,page):
        #页码从0开始
        a=int(page)+1
        b=25*a
        URL='http://pt.vm.fudan.edu.cn/index.php?action=torrents;xml;sa=data&sEcho='+str(a)+'&iColumns=27&sColumns=board%2Ctopic%2Cimdb%2Cdouban%2Cposter%2Cname%2Csubname%2Csubject%2Cid%2Cmember%2Cuploader%2Ccodec%2Cres%2Csize%2Ctime%2Cupload%2Cdownload%2Cfinished%2Cupratio%2Cdownratio%2Cdetail%2CKeepingWeight%2CSeedingWeight%2Csort%2Cfavorite%2Creward%2Cexpire&iDisplayStart='+str(b)+"&iDisplayLength=25&sSearch=&bEscapeRegex=true&sSearch_0=&bEscapeRegex_0=true&bSearchable_0=false&sSearch_1=&bEscapeRegex_1=true&bSearchable_1=false&sSearch_2=&bEscapeRegex_2=true&bSearchable_2=false&sSearch_3=&bEscapeRegex_3=true&bSearchable_3=false&sSearch_4=&bEscapeRegex_4=true&bSearchable_4=false&sSearch_5=&bEscapeRegex_5=true&bSearchable_5=true&sSearch_6=&bEscapeRegex_6=true&bSearchable_6=true&sSearch_7=&bEscapeRegex_7=true&bSearchable_7=true&sSearch_8=&bEscapeRegex_8=true&bSearchable_8=false&sSearch_9=&bEscapeRegex_9=true&bSearchable_9=false&sSearch_10=&bEscapeRegex_10=true&bSearchable_10=false&sSearch_11=&bEscapeRegex_11=true&bSearchable_11=false&sSearch_12=&bEscapeRegex_12=true&bSearchable_12=false&sSearch_13=&bEscapeRegex_13=true&bSearchable_13=false&sSearch_14=&bEscapeRegex_14=true&bSearchable_14=false&sSearch_15=&bEscapeRegex_15=true&bSearchable_15=false&sSearch_16=&bEscapeRegex_16=true&bSearchable_16=false&sSearch_17=&bEscapeRegex_17=true&bSearchable_17=false&sSearch_18=&bEscapeRegex_18=true&bSearchable_18=false&sSearch_19=&bEscapeRegex_19=true&bSearchable_19=false&sSearch_20=&bEscapeRegex_20=true&bSearchable_20=false&sSearch_21=&bEscapeRegex_21=true&bSearchable_21=false&sSearch_22=&bEscapeRegex_22=true&bSearchable_22=false&sSearch_23=&bEscapeRegex_23=true&bSearchable_23=false&sSearch_24=&bEscapeRegex_24=true&bSearchable_24=false&sSearch_25=&bEscapeRegex_25=true&bSearchable_25=false&sSearch_26=&bEscapeRegex_26=true&bSearchable_26=false&iSortingCols=1&iSortCol_0=14&sSortDir_0=desc&bSortable_0=false&bSortable_1=false&bSortable_2=false&bSortable_3=false&bSortable_4=false&bSortable_5=false&bSortable_6=false&bSortable_7=false&bSortable_8=false&bSortable_9=false&bSortable_10=true&bSortable_11=false&bSortable_12=false&bSortable_13=true&bSortable_14=true&bSortable_15=true&bSortable_16=true&bSortable_17=true&bSortable_18=false&bSortable_19=false&bSortable_20=false&bSortable_21=false&bSortable_22=false&bSortable_23=false&bSortable_24=false&bSortable_25=false&bSortable_26=false&isFree=0"
        res=json.loads(self.opener.open(URL).read())
        for t_no in filter(self.filter_func,res['aaData']):
            self.down_torrent(t_no)

    def down_torrent(self,t_no):
        p=os.path.join(self.config.save_path,t_no[0])+".torrent"
        print t_no
        if not os.path.isfile(p):
            url="http://pt.vm.fudan.edu.cn/index.php?action=dltorrent;id="+str(t_no[0])
            f=open(os.path.join(self.config.save_path,t_no[0])+".torrent","wb")
            f.write(self.opener.open(url).read())
            f.close()
            self.tc.download(p)

t=torrent_checker()
t.login()
t.down_page(0)
