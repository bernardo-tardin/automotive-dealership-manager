import json
from datetime import datetime
from operator import itemgetter
import os

class Installments():

    def __init__(self):
        dir = os.path.dirname(__file__)
        dir += "/database.json"
        f = open(dir)
        self.data = json.load(f)
        f.close()
        self.installments=[]

    def verifyClients(self):
        for cliente in self.data['clientes']:
            cl={}
            cl['nome'] = cliente['name']
            for prestacao in cliente['prestacoes']:
                date = datetime.strptime(prestacao[1],'%d-%m-%Y')
                dif = date - datetime.today()
                difference = str(dif.days).split(' ')
                prestacao.append(int(difference[0]))
            newPrestacaoList = sorted(cliente['prestacoes'], key=itemgetter(4))
            cl['prestacoes'] = newPrestacaoList
            self.installments.append(cl)
        return self.installments
    
    def differenceDate(self):
        self.onlyInstallments=[]
        for cliente in self.installments:
            for prestacao in cliente['prestacoes']:
                cl = []
                cl.append(cliente['nome'])
                for data in prestacao:
                    cl.append(data)
                self.onlyInstallments.append(cl)
        self.onlyInstallments = sorted(self.onlyInstallments, key=itemgetter(5))
        return self.onlyInstallments
    
    def under30(self):
        self.listUnder30=[]
        for prestacao in self.onlyInstallments:
            if prestacao[5] <= 30:
                self.listUnder30.append(prestacao)
        return self.listUnder30

