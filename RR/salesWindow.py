import PySimpleGUI as sg
import json
import simulationWindow as sw
from datetime import datetime, date
import os
import salesPDF as spdf
from dateutil.relativedelta import relativedelta
import receiptsEntradaPDF as rpdf

class Sales():
    

    def __init__(self):
        self.dir = os.path.dirname(__file__)
        dir = self.dir + "/database.json"
        f = open(dir)
        self.data = json.load(f)
        f.close()

    def createInstallments(self,valor_total,juros,valor_entrada,n_prestacoes,data_inicio):
        calculo = sw.Simulation(valor_total,juros,valor_entrada,n_prestacoes)
        valor_prestacao = calculo.calculateInstallments()
        self.prestacoes = []
        for i in range(1,n_prestacoes+1):
            prestacao=[]
            prestacao.append(i)
            prestacao.append((data_inicio + relativedelta(months=i)).strftime("%d-%m-%Y"))
            prestacao.append(valor_prestacao)
            prestacao.append('Nao Pago')
            self.prestacoes.append(prestacao)
        return self.prestacoes
    
    def makeSale(self,name,nif,telephone,email,morada,localidade,codigo_postal,identificacao,matricula,marca,modelo,ano,valor_total,juros,valor_entrada,n_prestacoes,data_inicio):
        cliente={}
        cliente['data'] = (date.today()).strftime('%d-%m-%Y')
        cliente['name'] = name
        cliente['nif'] = nif
        cliente['telephone'] = telephone
        cliente['email'] = email
        cliente['morada'] = morada
        cliente['localidade'] = localidade
        cliente['codigo_postal'] = codigo_postal
        cliente['identificacao'] = identificacao
        cliente['matricula'] = matricula
        cliente['marca'] = marca
        cliente['modelo'] = modelo
        cliente['ano'] = ano
        cliente['valor_total'] = valor_total
        cliente['valor_entrada'] = valor_entrada
        cliente['juros'] = juros
        cliente['prestacoes'] = self.createInstallments(valor_total,juros,valor_entrada,n_prestacoes,data_inicio)
        self.data['clientes'].append(cliente)
        json_object = json.dumps(self.data,indent=2)
        with open(self.dir + '/database.json','w') as outfile:
            outfile.write(json_object)
        return self.data
    
    
    
class salesInterface():
    
    sg.theme('LightGrey1')

    def __init__(self):

        self.toprow=['Número da prestação','Data de vencimento','Valor','Estado']
        self.rows=[]

        layout = [[sg.Text('Dados do cliente')],
                    [sg.Text('Nome:'),sg.Input(key='-name'), sg.Text('NIF:'),sg.Input(key='-NIF-',size=(20,5))],
                    [sg.Text('Telemóvel:'),sg.Input(key='-telephone',size=(20,5)),sg.Text('Email:'),sg.Input(key='-email')],
                    [sg.Text('Morada:'),sg.Input(key='-MORADA-'),sg.Text('Localidade:'),sg.Input(key='-LOCALIDADE-',size=(20,5)),sg.Text('Código Postal:'),sg.Input(key='-CODIGO-',size=(20,5))],
                    [sg.Text('Documento de Identificação:'),sg.Radio('Cartão de Cidadão','IDENTIFICACAO',default=False,key='-CC-'),sg.Radio('Título de Residência','IDENTIFICACAO',default=False,key='-TR-'),sg.Radio('Passaporte','IDENTIFICACAO',default=False,key='-PASSAPORTE-'),sg.Input(key='-IDENTIFACAO-')],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Dados do automóvel')],
                    [sg.Text('Matrícula:'),sg.Input(key='-MATRICULA-',size=(20,5)),sg.Text('Marca:'),sg.Input(key='-MARCA-',size=(20,5))],
                    [sg.Text('Modelo:'),sg.Input(key='-MODELO-',size=(20,5)),sg.Text('Ano:'),sg.Input(key='-ANO-',size=(10,5))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Condições da compra')],
                    [sg.Text('Valor total:'), sg.Input(key='-valor_total',size=(20,5)),sg.Text('Valor de entrada:'),sg.Input(key='-entrada',size=(20,5)),sg.Button('Gerar Recibo',visible=False,key='-RECIBO-')],
                    [sg.Text('Juros (% ao mês)'),sg.Input(key='-juros',size=(20,5)),sg.Text('Número de prestações:'),sg.Input(key='-n_prestacoes',size=(20,5)),sg.Text('Data de ínicio:'),sg.Input(key='-date',size=(20,5)),sg.CalendarButton("Escolher data",close_when_date_chosen=True,target='-date')],
                    [sg.Button('Gerar Parcelas', key='-gerar')],
                    [sg.Table(values=self.rows,headings=self.toprow,auto_size_columns=True,justification='center',key='-table')],
                    [sg.Button('Confirmar Venda', key='-confirmar')]]
        
        self.window = sg.Window("Venda",layout=layout)

        self.dir = os.path.dirname(__file__)
        dir = self.dir + "/database.json"
        f = open(dir)
        self.data = json.load(f)
        f.close()

    def createSalesInterface(self):
        while True:
            self.event, self.values = self.window.read()
            if self.event == sg.WINDOW_CLOSED:
                break
            if self.event == '-gerar':
                self.rows=[]
                self.window['-table'].update(values=self.rows)
                pr = Sales()
                if self.values['-valor_total'] == '':
                    sg.popup('Indicar o valor total',title='ERRO')
                elif self.values['-juros'] == '':
                    sg.popup('Indicar a taxa de juros',title='ERRO')
                elif self.values['-n_prestacoes'] == '':
                    sg.popup('Indicar o número de prestações', title='ERRO')
                elif self.values['-date'] == '':
                    sg.popup('Indicar a data de ínicio das prestações', title='ERRO')
                else:
                    if self.values['-entrada'] == '':
                        self.values['-entrada'] = 0
                    else:
                        self.window['-RECIBO-'].update(visible=True)
                    prestacoes = pr.createInstallments(float(self.values['-valor_total']),float(self.values['-juros']),float(self.values['-entrada']),int(self.values['-n_prestacoes']),datetime.strptime(self.values['-date'],'%Y-%m-%d %H:%M:%S'))
                    for row in prestacoes:
                        self.rows.append(row)
                    self.window['-table'].update(values=self.rows)
            if self.event == '-RECIBO-':
                recibo = rpdf.ReceiptsPDF()
                recibo.conteudo(self.values['-name'],self.values['-NIF-'],self.values['-entrada'],self.values['-MARCA-'],self.values['-MODELO-'],self.values['-MATRICULA-'])
                self.data['transacoes'][0] += float(self.values['-entrada'])
                transacao=[]
                transacao.append(self.values['-name'])
                transacao.append('Entrada')
                transacao.append((date.today()).strftime('%d-%m-%Y'))
                transacao.append(float(self.values['-entrada']))
                self.data['transacoes'][1].append(transacao)
                json_object = json.dumps(self.data,indent=2)
                with open(self.dir + '/database.json','w') as outfile:
                    outfile.write(json_object)
            if self.event == '-confirmar':
                conf = Sales()
                if self.values['-valor_total'] == '':
                    sg.popup('Indicar o valor total',title='ERRO')
                elif self.values['-juros'] == '':
                    sg.popup('Indicar a taxa de juros',title='ERRO')
                elif self.values['-n_prestacoes'] == '':
                    sg.popup('Indicar o número de prestações', title='ERRO')
                elif self.values['-date'] == '':
                    sg.popup('Indicar a data de ínicio das prestações', title='ERRO')
                else:
                    if self.values['-entrada'] == '':
                        self.values['-entrada'] = 0
                    if self.values['-CC-'] == True:
                        self.identifacao = 'Cartão de Cidadão: ' + self.values['-IDENTIFACAO-']
                    if self.values['-TR-'] == True:
                        self.identifacao = 'Título de Residência: ' + self.values['-IDENTIFACAO-']
                    if self.values['-PASSAPORTE-'] == True:
                        self.identifacao = 'Passaporte: ' + self.values['-IDENTIFACAO-']
                    conf.makeSale(self.values['-name'],self.values['-NIF-'],self.values['-telephone'],self.values['-email'],self.values['-MORADA-'],self.values['-LOCALIDADE-'],self.values['-CODIGO-'],self.identifacao,self.values['-MATRICULA-'],self.values['-MARCA-'],self.values['-MODELO-'],self.values['-ANO-'],float(self.values['-valor_total']),float(self.values['-juros']),float(self.values['-entrada']),int(self.values['-n_prestacoes']),datetime.strptime(self.values['-date'],'%Y-%m-%d %H:%M:%S'))
                    venda = spdf.SalesPDF()
                    venda.conteudo(self.values['-name'],self.values['-NIF-'],self.values['-telephone'],self.values['-email'],self.values['-MORADA-'],self.values['-LOCALIDADE-'],self.values['-CODIGO-'],self.identifacao,self.values['-MATRICULA-'],self.values['-MARCA-'],self.values['-MODELO-'],self.values['-ANO-'],self.values['-valor_total'],str(self.values['-entrada']),self.values['-n_prestacoes'],self.rows)
                    self.window.close()
