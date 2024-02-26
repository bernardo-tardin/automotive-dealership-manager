import PySimpleGUI as sg
import simulationWindow as sw
import salesWindow as sl
import controlInstallments as cl
import json
from datetime import datetime
import cashierWindow as cs
import receiptsPrestacaoPDF as rpdf
import transactionsWindow as tw
import os
import alterarWindow as alt

class mainWindow():
    sg.theme('LightGrey1')
    
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        dir = self.dir + "/database.json"
        f = open(dir)
        self.data = json.load(f)
        f.close()

        self.rows=[]
        self.toprows=['Nº','Data','Valor','Estado']

        self.rows_right=[]
        self.toprows_right = ['Nome','Nº', 'Data', 'Valor']

        prst = cl.Installments()
        prst1 = prst.verifyClients()
        prst2 = prst.differenceDate()
        prst3 = prst.under30()

        for prest in prst3:
            self.rows_right.append(prest)
        
        left_column = [[sg.Image(self.dir + '/test.png')],[sg.HorizontalSeparator()],[sg.Button('Simulação', key='-simulation',font='Heveltica 20',auto_size_button=True,pad=(10,10))],[sg.Button('Venda',key='-venda',auto_size_button=True,font='Heveltica 20')],[sg.Button('Caixa',key='-caixa',auto_size_button=True,font='Heveltica 20')],[sg.Button('Alterar',key='-alterar',auto_size_button=True,font='Helvetica 20')],[sg.Button('Transações', key='-transacoes',auto_size_button=True, font='Helvetica 20')]]
        
        middle_column = [[sg.Text('Procurar cliente',font=('Helvetica',16,'bold'),justification='center')],
                         [sg.Text('Nome do cliente:',font=('Helvetica',12,'bold')), sg.Input(key='-nome',size=(40,5)), sg.Button('Procurar', key='-procurar',font='Helvetica 12')],
                         [sg.Text('Nome do cliente:', key='-NOME-',visible=False,font=('Helvetica',10,'bold')),sg.Text(key='-NAME-',visible=False,font=('Helvetica',10)),sg.Text('NIF:',visible=False,key='-NIF-',font=('Helvetica',10,'bold')),sg.Text(key='_NIF_',visible=False,font=('Helvetica',10))],
                         [sg.Text('Telemóvel:',key='-TELEFONE-',visible=False,font=('Helvetica',10,'bold')),sg.Text(key='-TELEMOVEL-',visible=False,font=('Helvetica',10)),sg.Text('Email:',visible=False,key='-EMAIL-',font=('Helvetica',10,'bold')),sg.Text(key='_EMAIL_',visible=False,font=('Helvetica',10))],
                         [sg.Text('Morada:',visible=False,key='-MORADA-',font=('Helvetica',10,'bold')),sg.Text(key='_MORADA_',visible=False,font=('Helvetica',10)),sg.Text('Código Postal:',visible=False,key='-CP-',font=('Helvetica',10,'bold')),sg.Text(key='-CODIGO-',visible=False,font=('Helvetica',10))],
                         [sg.Text('Marca:',visible=False,key='-MARCA-',font=('Helvetica',10,'bold')),sg.Text(key='_MARCA_',visible=False,font=('Helvetica',10)),sg.Text('Modelo:',key='-MODELO-',visible=False,font=('Helvetica',10,'bold')),sg.Text(key='_MODELO_',visible=False,font=('Helvetica',10)),sg.Text('Ano:',visible=False,key='-ANO-',font=('Helvetica',10,'bold')),sg.Text(key='_ANO_',visible=False,font=('Helvetica',10)),sg.Text('Matrícula:',visible=False,key='-MATRICULA-',font=('Helvetica',10,'bold')),sg.Text(key='_MATRICULA_',visible=False,font=('Helvetica',10))],
                         [sg.Table(values=self.rows,headings=self.toprows,key='-table',enable_events=True,enable_click_events=True,expand_x=True,font='Helvetica 12',auto_size_columns=True,justification='center')],
                         [sg.Text('Nº da prestação:',font=('Helvetica',12,'bold')),sg.Text(key='-n_parcela'),sg.Text('Vencimento:',font=('Helvetica',12,'bold')),sg.Text(key='-vencimento'),sg.Text('Valor:',font=('Helvetica',12,'bold')),sg.Text(key='-valor'),sg.Text('Estado:',font=('Helvetica',12,'bold')),sg.Radio('Pago', 'PAGAMENTO',default=False,key='-pago',font=('Helvetica',12)),sg.Radio('Não Pago','PAGAMENTO', default=True,key='-nao',font=('Helvetica',12))],
                         [sg.Button('Salvar Alterações', key='-salvar', auto_size_button=True, font='Helvetica 12')],
                         [sg.HorizontalSeparator()],
                         [sg.Text('Caixa Atual:',font=('Helvetica',16)),sg.Text(round(self.data['transacoes'][0],2),key='-total',font=('Helvetica',16,'bold'))]]

        right_column = [[sg.Text('Prestações a vencer/vencidas:',font=('Helvetica',16,'bold'))],
                        [sg.Table(values=self.rows_right, headings=self.toprows_right,key='-right_table')]]
        
        layout=[[sg.Column(layout=left_column,expand_x=True,expand_y=True,vertical_alignment='center'),sg.VerticalSeparator(),
                sg.Column(layout=middle_column,expand_x=True,expand_y=True),sg.VerticalSeparator(),
                sg.Column(layout=right_column,expand_x=True,expand_y=True)]]

        self.window = sg.Window('RR Motors',layout=layout)


    def createInterface(self):

        while True:

            dir = os.path.dirname(__file__)
            dir += "/database.json"
            f = open(dir)
            self.data = json.load(f)
            f.close()

            self.event, self.value = self.window.read()

            self.window['-total'].update(round(self.data['transacoes'][0],2))

        
            prst = cl.Installments()
            prst.verifyClients()
            prst.differenceDate()
            prst3 = prst.under30()
            for prest in prst3:
                self.rows_right.append(prest)
            

            if self.event == sg.WINDOW_CLOSED:
                break
            if self.event == '-simulation':
                simulation = sw.simulationInterface()
                simulation.createInterfaceSimulation()
            if self.event == '-venda':
                venda = sl.salesInterface()
                venda.createSalesInterface()
            if self.event == '-procurar':
                encontrado = False
                self.rows=[]
                self.window['-table'].update(values=self.rows)
                if self.value['-nome'] == '':
                    sg.popup('Nenhum nome escrito', title='ERRO')
                else:
                    for cliente in self.data['clientes']:
                        if self.value['-nome'].lower() in cliente['name'].lower():
                            encontrado = True
                            self.window['-NOME-'].update(visible=True)
                            self.window['-NAME-'].update(cliente['name'])
                            self.window['-NAME-'].update(visible=True)
                            self.window['-NIF-'].update(visible=True)
                            self.window['_NIF_'].update(cliente['nif'])
                            self.window['_NIF_'].update(visible=True)
                            self.window['-TELEFONE-'].update(visible=True)
                            self.window['-TELEMOVEL-'].update(cliente['telephone'])
                            self.window['-TELEMOVEL-'].update(visible=True)
                            self.window['-EMAIL-'].update(visible=True)
                            self.window['_EMAIL_'].update(cliente['email'])
                            self.window['_EMAIL_'].update(visible=True)
                            self.window['-MORADA-'].update(visible=True)
                            self.window['_MORADA_'].update(cliente['morada'])
                            self.window['_MORADA_'].update(visible=True)
                            self.window['-CP-'].update(visible=True)
                            self.window['-CODIGO-'].update(cliente['codigo_postal'])
                            self.window['-CODIGO-'].update(visible=True)
                            self.window['-MARCA-'].update(visible=True)
                            self.window['_MARCA_'].update(cliente['marca'])
                            self.window['_MARCA_'].update(visible=True)
                            self.window['-MODELO-'].update(visible=True)
                            self.window['_MODELO_'].update(cliente['modelo'])
                            self.window['_MODELO_'].update(visible=True)
                            self.window['-ANO-'].update(visible=True)
                            self.window['_ANO_'].update(cliente['ano'])
                            self.window['_ANO_'].update(visible=True)
                            if cliente['prestacoes'] == []:
                                sg.popup('Cliente sem prestações',title='ERRO')
                            else:
                                for prestacao in cliente['prestacoes']:
                                    self.rows.append(prestacao)
                                self.window['-table'].update(values=self.rows)
                    if not encontrado:
                        sg.popup('Cliente não encontrado', title='ERRO')
            if self.value['-table'] != []:
                indice = self.value['-table'][0]
                self.window['-n_parcela'].update(self.rows[indice][0])
                self.window['-vencimento'].update(self.rows[indice][1])
                self.window['-valor'].update(self.rows[indice][2])
                estado = self.rows[indice][3]
                if estado == 'Nao Pago':
                    self.window['-nao'].update(True)
                if self.value['-pago'] == True:
                    if self.event == '-salvar':
                        self.window['-nao'].update(False)
                        indice = self.value['-table'][0]
                        for cliente in self.data['clientes']:
                            if self.value['-nome'].lower() in cliente['name'].lower():
                                recibo = rpdf.ReceiptsPDF()
                                recibo.conteudo(cliente['name'],cliente['nif'],self.rows[indice][2],cliente['marca'],cliente['modelo'],cliente['matricula'])
                                self.data['transacoes'][0] += float(self.rows[indice][2])
                                self.rows[indice][3] = 'Pago'
                                self.rows[indice].insert(0,cliente['name'])
                                date = datetime.today()
                                self.rows[indice].append(date.strftime("%d-%m-%Y"))
                                self.data['transacoes'][1].append(self.rows[indice])
                                self.rows.pop(indice)
                                self.window['-table'].update(values=self.rows)
                                cliente['prestacoes'].pop(indice)
                                json_object = json.dumps(self.data,indent=2)
                                with open(self.dir+'/database.json','w') as outfile:
                                    outfile.write(json_object)
                                self.rows_right = []
                                self.window['-right_table'].update(values=self.rows_right)
                                prst = cl.Installments()
                                prst.verifyClients()
                                prst.differenceDate()
                                prst3 = prst.under30()
                                for prest in prst3:
                                    self.rows_right.append(prest)
                                self.window['-right_table'].update(values=self.rows_right)
                    self.window['-pago'].update(False)
                    self.window['-n_parcela'].update('')
                    self.window['-vencimento'].update('')
                    self.window['-valor'].update('')
            if self.event == '-caixa':
                caixa = cs.cashierInterface()
                caixa.createInterface()
            if self.event == '-transacoes':
                transactions = tw.Transactions()
                transactions.interface()
            if self.event == '-alterar':
                alterar = alt.Alterar()
                alterar.interfaceAlterar()



interface = mainWindow()
interface.createInterface()