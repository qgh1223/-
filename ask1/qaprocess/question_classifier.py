from ask1.dbopt.neoaddopt import NeoRelationOpt
from ask1.qaprocess.kmpmatch import kmp_search,getNext


class QuestionClassifier:
    def __init__(self):
        self.dictionary={
            'symptom_qwds':['症状', '表征', '现象', '症候', '表现',' 症状表现'],
            'cause_qwds':['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成'],
            'acompany_qwds':['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现',' 并发疾病'],
            'food_qwds':['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品'],
            'drug_qwds':['药', '药品', '用药', '胶囊', '口服液', '炎片',' 常用药物'],
            'prevent_qwds':['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                            '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                            '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                            '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                            '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不'],
            'lasttime_qwds':['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年',' 治疗周期'],
            'cureway_qwds':['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治'],
            'cureprob_qwds':['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医',' 治愈率'],
            'easyget_qwds':['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上',' 易感人群'],
            'check_qwds':['检查', '检查项目', '查出', '检查', '测出', '试出',' 常用检查'],
            'belong_qwds':['属于什么科', '属于', '什么科', '科室',' 就诊科室'],
            'cure_qwds':['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                         '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        }
    def get_class(self,question):
        for keyword in self.dictionary:
            for word in self.dictionary[keyword]:
                next=[]
                getNext(word,next)
                if(kmp_search(question,word,next)==1):
                    return keyword
    def get_disease_name(self,question):
        diseaselist=NeoRelationOpt('','','').query_disease()
        for disease in diseaselist:
            next=[]
            getNext(disease,next)
            if(kmp_search(question,disease,next)==1):
                return disease
        return ''