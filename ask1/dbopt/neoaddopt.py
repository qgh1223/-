from neo4j.v1 import Graph,GraphDatabase
from keras.applications.inception_v3 import InceptionV3
class NeoRelationOpt:
    def __init__(self,
                 disease,relation,value,question=None,
                 uri='bolt://localhost:11002',
                 username='neo4j',password='188992zjl',
                 port='11002'):
        self.driver=GraphDatabase.driver(uri,auth=(username,password))
        self.disease=disease
        self.relation=relation
        self.value=value
        self.question=question
    def exists_disease(self,tx):
        cql='''
        match (d:Disease)
        where d.value=$disease
        return d
        '''
        i=0
        for record in tx.run(cql,disease=self.disease):
            i+=1
            break
        return i
    def add_graph1(self,tx):
        cql='''
        create (p:Disease {value:$disease})-[r:Relation {value:$relation}]->(v:Value {value:$value})
        '''
        tx.run(cql,disease=self.disease,relation=self.relation,
               value=self.value)
    def add_graph2(self,tx):
        cql='''
        match (p:Disease)
        where p.value=$disease
        create (p)-[r:Relation {value:$relation}]->(v:Value {value:$value})
        '''
        tx.run(cql,disease=self.disease,relation=self.relation,
               value=self.value)
    def add_opt(self):
        with self.driver.session() as session:
            if(session.write_transaction(self.exists_disease)==0):
                session.write_transaction(self.add_graph1)
            else:
                session.write_transaction(self.add_graph2)
    def query_all_disease(self,tx):
        cql='''
        match (p:Disease)
        return p.value
        '''
        diseaselist=[]
        for record in tx.run(cql):
            diseaselist.append(record['p.value'])
        return diseaselist
    def query_disease(self):
        with self.driver.session() as session:
            diseaselist=session.write_transaction(self.query_all_disease)
        return diseaselist
    def query_value(self,tx):
        cql='''
        match (p:Disease)-[r:Relation]-(q:Value)
        where p.value=$disease and r.value=$relation
        return q.value
        '''
        for record in tx.run(cql,disease=self.disease,relation=self.relation):
            return record['q.value']
    def query_value_opt(self):
        with self.driver.session() as session:
            value=session.write_transaction(self.query_value)
            return value
    def add_new_question(self,tx):
        cql='''
        create (p:Question {value:$value})
        '''
        tx.run(cql,value=self.question)
    def add_new_question_opt(self):
        with self.driver.session() as session:
            session.write_transaction(self.add_new_question)
    def exists_symptom(self,symptom):
        cql='''
        match (p:Symptom)
        where p.value=$symptom
        return p
        '''
