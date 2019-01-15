import datetime
import time

from ask1.dbopt.neoaddopt import NeoRelationOpt
from ask1.qaprocess.question_classifier import QuestionClassifier


def answer_generate(question):
    diseasename=QuestionClassifier().get_disease_name(question)
    questiontype=QuestionClassifier().get_class(question)
    if(diseasename==''):
        answer ='该疾病暂时未收入，请转人工'
    else:
        if(questiontype=='symptom_qwds'):
            relation='症状表现'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer='{0}的症状包括：{1}'.format(diseasename,value)
        elif(questiontype=='acompany_qwds'):
            relation='并发疾病'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer = '症状{0}可能染上的疾病有：{1}'.format(diseasename,value)
        elif(questiontype=='drug_qwds'):
            relation='常用药物'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            if(value==None):
                answer='{0}暂时没有推荐药物'
            else:
                answer = '{0}通常的使用的药品包括：{1}'.format(diseasename,value)
        elif(questiontype=='lasttime_qwds'):
            relation='治疗周期'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer = '{0}治疗可能持续的周期为：{1}'.format(diseasename,value)
        elif(questiontype=='cureprob_qwds'):
            relation='治愈率'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer = '{0}治愈的概率为（仅供参考）：{1}'.format(diseasename,value)
        elif(questiontype=='easyget_qwds'):
            relation='易感人群'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer = '{0}的易感人群包括：{1}'.format(diseasename,value)
        elif(questiontype=='check_qwds'):
            relation='常用检查'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer = '{0}通常可以通过以下方式检查出来：{1}'.format(diseasename,value)
        elif(questiontype=='belong_qwds'):
            relation='就诊科室'
            value=NeoRelationOpt(diseasename,relation,'').query_value_opt()
            answer = '{0}就诊科室：{1}'.format(diseasename,value)
        else:
            answer='暂时不能回答，请转人工'
    return answer
'''while(True):
    print('请输入问题：')

    question=input()
    start=time.time()
    if(question=='end'):
        break
    answer=answer_generate(question)
    print('robot：'+answer)
    end=time.time()
    #print(end-start)
'''




