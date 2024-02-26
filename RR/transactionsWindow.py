import os
import json
import  PySimpleGUI as sg
from datetime import datetime
from operator import itemgetter
import csv
#import jpype
#import asposecells
#jpype.startJVM()
#from asposecells.api import Workbook, LoadOptions, SaveFormat


class Transactions():
    sg.theme('LightGrey1')

    def __init__(self):
        self.dir = os.path.dirname(__file__)
        self.dir += "/database.json"
        f = open(self.dir)
        self.data = json.load(f)
        f.close()

        self.top_rows_sales = ["Data","Cliente","Valor","Número de prestações","Marca","Modelo","Matrícula",]
        self.top_rows_transactions = ["Data","Descrição","Valor"]
        self.top_rows_entries = ["Data","Descrição","Valor"]
        self.top_rows_exits = ["Data","Descrição","Valor"]

        self.sales=[]
        if self.data['clientes'] != []:
            for elem in self.data['clientes']:
                cliente=[]
                cliente.append(elem['data'])
                cliente.append(elem['name'])
                cliente.append(elem['valor_total'])
                cliente.append(len(elem['prestacoes']))
                cliente.append(elem['marca'])
                cliente.append(elem['modelo'])
                cliente.append(elem['matricula'])
                self.sales.append(cliente)

        self.entries=[]
        if self.data['transacoes'][1] != []:
            for elem in self.data['transacoes'][1]:
                if len(elem) >= 4:
                    if elem[3] > 0:
                        entrada = []
                        if len(elem) == 4:
                            entrada.append(elem[2])
                            entrada.append(f"Entrada dada pelo cliente {elem[0]}")
                            entrada.append(elem[3])
                            self.entries.append(entrada)
                        if len(elem) == 6:
                            entrada.append(elem[5])
                            entrada.append(f"Pagamento da prestação {str(elem[1])} pelo cliente {elem[0]}")
                            entrada.append(elem[3])
                            self.entries.append(entrada)
                else:
                    if elem[2] > 0:
                        entrada = []
                        entrada.append(elem[0])
                        entrada.append(elem[1])
                        entrada.append(elem[2])
                        self.entries.append(entrada)

        self.exits=[]
        if self.data['transacoes'][1] != []:
            for elem in self.data['transacoes'][1]:
                if len(elem) == 3:
                    if elem[2] < 0:
                        exit=[]
                        exit.append(elem[0])
                        exit.append(elem[1])
                        exit.append(elem[2])
                        self.exits.append(exit)

        transactions = []
        if self.entries != []:
            for elem in self.entries:
                elem[0] = datetime.strptime(elem[0],'%d-%m-%Y')
                transactions.append(elem)
        if self.exits != []:
            for elem in self.exits:
                elem[0] = datetime.strptime(elem[0],'%d-%m-%Y')
                transactions.append(elem)
        if transactions != []:
            self.transactions = sorted(transactions,key=itemgetter(0))
            for elem in self.transactions:
                elem[0] = elem[0].strftime('%d-%m-%Y')
        else:
            self.transactions=[]
        

        layout=[
            [sg.Text('Parâmetros:',font=('Helvetica',12,'bold')),sg.OptionMenu(values=['Transações','Vendas','Entradas','Saídas'],key='-OPTION-'),sg.Button('Procurar',key='-PROCURAR-')],
            [sg.Table(values=self.sales,headings=self.top_rows_sales,visible=False,key='-VENDAS-')],
            [sg.Table(values=self.entries,headings=self.top_rows_entries,visible=False,key='-ENTRADAS-')],
            [sg.Table(values=self.exits,headings=self.top_rows_exits,visible=False,key='-SAÍDAS-')],
            [sg.Table(values=self.transactions,headings=self.top_rows_transactions,visible=False,key='-TRANSACOES-')],
            [sg.Button('Gerar Extrato', key='-EXTRATO-',visible=False)]
        ]

        self.window = sg.Window("Transações",layout=layout)
    
    def interface(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event == sg.WINDOW_CLOSED:
                break
            if self.event == '-PROCURAR-':
                self.window['-EXTRATO-'].update(visible=True)
                if self.values['-OPTION-'] == 'Transações':
                    self.window['-TRANSACOES-'].update(visible=True)
                    headers = self.top_rows_transactions
                    rows = self.transactions
                if self.values['-OPTION-'] == 'Vendas':
                    self.window['-VENDAS-'].update(visible=True)
                    headers = self.top_rows_sales
                    rows = self.sales
                if self.values['-OPTION-'] == 'Entradas':
                    self.window['-ENTRADAS-'].update(visible=True)
                    headers = self.top_rows_entries
                    rows = self.entries
                if self.values['-OPTION-'] == 'Saídas':
                    self.window['-SAÍDAS-'].update(visible=True)
                    headers = self.top_rows_exits
                    rows = self.exits
            if self.event == '-EXTRATO-':
                dir = os.path.dirname(__file__) + "/Extratos"
                initial_count = 0
                for path in os.listdir(dir):
                    if os.path.isfile(os.path.join(dir, path)):
                        initial_count += 1

                self.file_name_2 = dir + "/Extrato" + str(initial_count) + ".csv"
                
                with open(self.file_name_2, "w") as csvfile:
                    extrato = csv.writer(csvfile)
                    extrato.writerow(headers)
                    for row in rows:
                        extrato.writerow(row)

               # new_filename = self.file_name_2.replace('.csv','.xlsx')

               # loadOptions =  LoadOptions(FileFormatType.CSV)

               # workbook =  Workbook(self.file_name_2, loadOptions)

               # workbook.save(new_filename , SaveFormat.XLSX)

               # os.remove(self.file_name_2)
                
                #self.window.close()
            

