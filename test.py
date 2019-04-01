import pandas as pd
import requests
import re
import os 
import sys
import json
import csv
#视频AV号列表 
aid_list=[]
#评论用户极其信息
info_list=[]
#获取指定UP的所有视频的AV号 mid:用户编号 size:单次拉取数目 page:页数
def getAllAVList(mid,size,page):
    #获取up主视频列表
    for n in range(1,page+1):
        url="http://space.bilibili.com/ajax/member/getSubmitVideos?mid="+\
            str(mid)+"&pagesize="+str(size)+"&page="+str(n)
        r=requests.get(url)
        text=r.text
        json_text=json.loads(text)
#        print(json_text)
        for item in json_text["data"]["vlist"]:
            aid_list.append(item["aid"])
    print(aid_list)
#getAllAVList(31653614,5,8)
#获取一个AV号视频下所有评论
def getAllCommentList(item):
    url="http://api.bilibili.com/x/reply?type=1&oid=" + str(item) + "&pn=1&nohot=1&sort=0"
    r=requests.get(url)
    numtext=r.text
    json_text=json.loads(numtext)
    print(json_text)
    commentsNum=json_text['data']["page"]["count"]
    page=commentsNum//20+1
    for n in range(1,page):
        url="https://api.bilibili.com/x/v2/reply?jsonp&pn"+str(n)+"&type=1&oid="+str(item)+"&sort=1&nohot=1"
        req=requests.get(url)
        text=req.text
        json_text_list=json.loads(text)
        for i in json_text_list['data']["replies"]:
            info_list.append([i["member"]["uname"],i['member']['sex'],i["content"]["message"]])
            #print(info_list)

#def saveTxt(filename,filecontent):
#    filename=str(filename)+".txt"
#    for content in filecontent:
#        with open(filename,"a",encoding='utf8') as txt:
#            txt.write(content[0]+''+content[1].replace('\n','')+'\n\n')
#            print("文件写入中")
            
def saveTxt(item,filecontent):
    comments=pd.DataFrame(columns=['item','name','sex','comment'])
    for content in filecontent:
        t=pd.DataFrame([[item,content[0],content[1],content[2]]],columns=['item','name','sex','comment'])
        comments=pd.concat([comments,t])
    comments.to_csv(str(item)+".csv",encoding="utf-8")
    print("文件写入中")
            
#if __name__=="__main__":
#    getAllAVList(31653614,5,8)
#    all_comments=pd.DataFrame(columns=['item','name','sex','comment'])
#    for item in aid_list:
#        info_list.clear()
#        getAllCommentList(item)
#        saveTxt(item,info_list)
#        a=pd.read_csv(str(item)+".csv")
#        all_comments=pd.concat([all_comments,a])
#    all_comments.to_csv("all_comments.csv",encoding="utf-8")
help(pd.DataFrame.to_csv)
    