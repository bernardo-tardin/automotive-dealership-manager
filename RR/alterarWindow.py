import PySimpleGUI as sg
import json
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class Alterar():

    sg.theme('LightGrey1')

    def __init__(self):
        self.dir = os.path.dirname(__file__)
        dir = self.dir + "/database.json"
        f = open(dir)
        self.data = json.load(f)
        f.close()

    def interfaceAlterar(self):
        layout=[[sg.Text('Procurar cliente: '),sg.Input(key='-procurar'),sg.Button('Procurar',key='-button')],
                    [sg.Text('Dados do cliente')],
                    [sg.Text('Nome:'),sg.Input(key='-name'), sg.Text('NIF:'),sg.Input(key='-NIF-')],
                    [sg.Text('Telemóvel:'),sg.Input(key='-telephone'),sg.Text('Email:'),sg.Input(key='-email')],
                    [sg.Text('Morada:'),sg.Input(key='-MORADA-'),sg.Text('Localidade:'),sg.Input(key='-LOCALIDADE-'),sg.Text('Código Postal:'),sg.Input(key='-CODIGO-')],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Dados do automóvel')],
                    [sg.Text('Matrícula:'),sg.Input(key='-MATRICULA-'),sg.Text('Marca:'),sg.Input(key='-MARCA-')],
                    [sg.Text('Modelo:'),sg.Input(key='-MODELO-'),sg.Text('Ano:'),sg.Input(key='-ANO-')],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Condições da compra')],
                    [sg.Text('Valor total:'), sg.Input(key='-valor_total'),sg.Text('Valor de entrada:'),sg.Input(key='-entrada'),sg.Button('Gerar Recibo',visible=False,key='-RECIBO-')],
                    [sg.Text('Juros (% ao mês)'),sg.Input(key='-juros'),sg.Text('Data de ínicio:'),sg.Input(key='-date'),sg.CalendarButton("Escolher data",close_when_date_chosen=True,target='-date')],
                    [sg.Button('Confirmar Alterações', key='-confirmar')]]
        
        self.window = sg.Window("Alterar",layout=layout)

        while True:
            self.event, self.values = self.window.read()
            if self.event == sg.WINDOW_CLOSED:
                break
            if self.event == '-button':
                for cliente in self.data['clientes']:
                    if self.values['-procurar'].lower() in cliente['name'].lower():
                        self.window['-name'].update(cliente['name'])
                        self.window['-NIF-'].update(cliente['nif'])
                        self.window['-telephone'].update(cliente['telephone'])
                        self.window['-email'].update(cliente['email'])
                        self.window['-MORADA-'].update(cliente['morada'])
                        self.window['-LOCALIDADE-'].update(cliente['localidade'])
                        self.window['-CODIGO-'].update(cliente['codigo_postal'])
                        self.window['-MATRICULA-'].update(cliente['matricula'])
                        self.window['-MARCA-'].update(cliente['marca'])
                        self.window['-MODELO-'].update(cliente['modelo'])
                        self.window['-ANO-'].update(cliente['ano'])
                        self.window['-valor_total'].update(cliente['valor_total'])
                        self.window['-entrada'].update(cliente['valor_entrada'])
                        self.window['-juros'].update(cliente['juros'])
                        data_string = cliente['prestacoes'][0][1]
                        data_format = datetime.strptime(data_string,'%d-%m-%Y')
                        self.window['-date'].update(data_format)
            if self.event == '-confirmar':
                for cliente in self.data['clientes']:
                    if self.values['-procurar'].lower() in cliente['name'].lower():
                        cliente['name'] = self.values['-name']
                        cliente['nif'] = self.values['-NIF-']
                        cliente['telephone'] = self.values['-telephone']
                        cliente['email'] = self.values['-email']
                        cliente['morada'] = self.values['-MORADA-']
                        cliente['localidade'] = self.values['-LOCALIDADE-']
                        cliente['codigo_postal'] = self.values['-CODIGO-']
                        cliente['matricula'] = self.values['-MATRICULA-']
                        cliente['modelo'] = self.values['-MODELO-']
                        cliente['marca'] = self.values['-MARCA-']
                        cliente['ano'] = self.values['-ANO-']
                        cliente['valor_total'] = self.values['-valor_total']
                        cliente['valor_entrada'] = self.values['-entrada']
                        cliente['juros'] = self.values['-juros']
                        data_string = self.values['-date'][:10]
                        data_type = datetime.strptime(data_string,'%Y-%m-%d')
                        for i in range(len(cliente['prestacoes'])):
                            cliente['prestacoes'][i][1] = (data_type + relativedelta(months=i+1)).strftime("%d-%m-%Y")
                        json_object = json.dumps(self.data,indent=2)
                        with open(self.dir + '/database.json','w') as outfile:
                            outfile.write(json_object)
                        self.window.close()


                        