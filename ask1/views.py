import json
import time
import os
import datetime
import random
import pandas as pd

from django.shortcuts import render,HttpResponse

from ask1.dbopt.neoaddopt import NeoRelationOpt
from ask1.qaprocess.generate_answer import answer_generate


def home(request):
    string=u'hello world'
    return render(request,
                  '../templates/home1.html',{'string': string})
def index(request):

    return render(request,'../templates/index.html')
def chat(request):
    return render(request,'chat.html')
def getanswer(request):
    question=request.GET['question']
    start=time.time()
    answer=answer_generate(question)
    end=time.time()
    print(end-start)
    return HttpResponse(json.dumps(answer),
                        content_type='application/json')
def humananswer(request):
    question=request.GET['question']
    NeoRelationOpt('','','',question=question).add_new_question_opt()
def filedownload(request):
    file=open('ask1/resource/static/filetemplate.xls','rb')
    response=HttpResponse(file)
    response['Content_Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="filetemplate.xls"'
    return response
def uploadfile(request):
    obj=request.FILES.get('filename')
    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    randomNum=random.randint(0,100000)
    randomNum=str(0)+str(randomNum)
    uniqueNum=str(nowTime)+str(randomNum)
    filepath='ask1/resource/static/unsolved/question'+uniqueNum+'.csv'
    f=open(filepath,'wb')
    for chunk in obj.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse('ok')

def fileadddata(filepath):
    data=pd.read_csv(filepath)
    try:
        for i in range(len(data)):
            diseasename=data['疾病名'][i]
            relation=data['问题'][i]
            answer=data['答案'][i]
            NeoRelationOpt(diseasename,relation,answer).add_opt()
    except KeyError:
        print('文件格式错误')
def batchadd():
    BASE_DIR='ask1/resource/static/unsolved/'
    for path in os.listdir(BASE_DIR):
        filepath=BASE_DIR+path
        fileadddata(filepath)
        os.remove(filepath)