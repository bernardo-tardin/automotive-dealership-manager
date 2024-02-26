import json
import PySimpleGUI as sg
from datetime import datetime
import os

class cashierInterface():

    def __init__(self):
        
        sg.theme('LightGrey1')

        self.dir = os.path.dirname(__file__)
        self.dir += "/database.json"
        f = open(self.dir)
        self.data = json.load(f)
        f.close()

        layout=[[sg.Text('Caixa')],
                [sg.Text('Descrição:'), sg.Input(key='-descricao')],
                [sg.Text('Valor:'), sg.Input(key='-valor')],
                [sg.Button('Entrada',key='-entrada',button_color='green',),sg.Button('Saída', key='-saida',button_color='red')]]
        
        self.window = sg.Window('Caixa',layout=layout)

    def createInterface(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event == sg.WINDOW_CLOSED:
                break
            if self.event == '-entrada':
                transacao=[]
                date = datetime.today()
                transacao.append(date.strftime('%d-%m-%Y'))
                transacao.append(self.values['-descricao'])
                transacao.append(float(self.values['-valor']))
                self.data['transacoes'][0] += float(self.values['-valor'])
                self.data['transacoes'][1].append(transacao)
                json_object = json.dumps(self.data,indent=2)
                with open(self.dir,'w') as outfile:
                    outfile.write(json_object)
                self.window.close()
            if self.event == '-saida':
                transacao=[]
                transacao.append(self.values['-descricao'])
                transacao.append(-float(self.values['-valor']))
                date = datetime.today()
                transacao.append(date.strftime('%d-%m-%Y'))
                self.data['transacoes'][0] -= float(self.values['-valor'])
                self.data['transacoes'][1].append(transacao)
                json_object = json.dumps(self.data,indent=2)
                with open(self.dir,'w') as outfile:
                    outfile.write(json_object)
                self.window.close()

