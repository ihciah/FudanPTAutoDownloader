# -*- coding: utf-8 -*-
#判别种子是否下载

import transmissionrpc,base64
import cookielib, urllib2, urllib, re, hashlib, time, json, os
from multiprocessing.dummy import Pool as ThreadPool

class judge:
    def __init__(self,t_info,opener):
        self.flag=True
        self.upload_count=int(t_info[15])       #上传人数
        self.download_count=int(t_info[16] )    #下载人数
        self.finish_count=int(t_info[17])       #完成人数
        self.t_id=t_info[0]                     #种子ID
        self.topic_id=t_info[2]                 #帖子ID
        self.board_id=int(t_info[1])            #所属版面ID
        self.time=self.convert_time(t_info[14]) #种子上传时间，距离今天的天数
        self.size=self.convert_size(t_info[13]) #种子大小，以MB为单位
        self.opener=opener
        if self.time==-1 or self.size==-1:
            self.flag=False
    def convert_time(self,t):
        #返回距离今天的天数
        if t.find(u'昨天')!=-1:
            return 1
        if t.find(u'今天')!=-1:
            return 0
        if t.find(u'前天')!=-1:
            return 2
        if t[:4].isdigit():
            return int(time.time()-time.mktime(time.strptime(t[:10],'%Y-%m-%d')))/(3600*24)
        return -1
    def convert_size(self,s):
        #返回以MB计量的种子大小
        s=s.split(' ')
        size_dict={"GB":1024,"MB":1,"TB":1024000,"KB":0.001}
        if size_dict.has_key(s[1]):
            return int(float(s[0].replace(',',''))*size_dict[s[1]])
        return -1
    def get_series(self):
        #获取本种子对应的主题中的种子信息
        topic_url="http://pt.vm.fudan.edu.cn/index.php?topic="+str(self.topic_id)
        topic=self.opener.open(topic_url).read()
        p=re.compile(r'torrent="(\d+).*?</td>.*?<span>(.*?)<br/>.*?</td>.*?<span>(.*?) .*?</td>.*?<span>(.*?)</span></td>',re.DOTALL)
        torrents_string=p.findall(topic)
        return torrents_string #[('75856','925.59MB','2012-12-22','4/0/172' ), (...), ...]

    def judge(self):

        #通用过滤规则
        if self.flag==False:
            return False
        if self.board_id in [8,47,53]:
            #动漫板块不下载
            return False
        if self.board_id in [13,43,63]:
            #游戏板块不下载
            return False
        if self.upload_count>50:
            #只参与上传人数少于50的种子
            return False
        if self.time>180:
            #只参与半年内的种子
            return False

        #针对2天内的资源，可认为人数数据无意义
        if self.time<=2:
            #针对电影区
            if self.board_id in [23,24,25]:
                #大小在800M到4G之间且上传者在5个以内
                if self.size<4000 and self.size>800 and self.upload_count<=5:
                    return True
                #大小在800M到6G之间且上传者在2个以内且为最近资源
                if self.time==0 and self.size<6000 and self.size>800 and self.upload_count<=2:
                    return True
            #针对电视剧区
            if self.board_id in [17,27,29,28,19,48]:
                related_torrents=self.get_series() #获取所有关联种子信息
                person_count=reduce(lambda a,b:(a[0]+b[0],a[1]+b[1],a[2]+b[2]),map(lambda x:x[3].split('/'),related_torrents))
                person_count=map(lambda x:float(x)/len(related_torrents),person_count) #获取所有相关种子并将三个值取平均
                #根据统计往常下载量超过10个且当前上传者在2个以内
                if person_count[2]>10 and self.upload_count<=2:
                    return True
            #针对其他所有资源，只要是800M以内且上传者是2个以内，并且时间是最近的
            if self.size<800 and self.upload_count<=2  and self.time<=1:
                return True

        #针对2天以上，一周以内的资源，未完成
        if self.time<=7:
            pass
        #针对7天以上，30天以内的资源，未完成
        if self.time<30:
            pass
        #针对30天~180天的资源，未完成
        pass
        return False



