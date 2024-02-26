import PySimpleGUI as sg
import simulationPDF as spdf

class Simulation():
    def __init__(self,total,fees,entry,installments):
        self.total = total - entry
        if fees != 0:
            self.fees = fees/100
        else:
            self.fees = 0
        self.installments = installments
        self.listAmortization = []
        self.listBalanceDue = []
        self.listFees = []


    def calculateInstallments(self):
        if self.fees != 0:
            self.eachInstallment = round((self.total * (self.fees)) / (1 - (1/(1+(self.fees))**self.installments)),2)
        else:
            self.eachInstallment = round((self.total/self.installments),2)
        return self.eachInstallment
    
    def amortization(self):
        if self.fees != 0:
            a1 = round((self.eachInstallment-(self.total * (self.fees))),2)
            for i in range(self.installments+1):
                if i == 0:
                    self.listAmortization.append(0)
                elif i == 1:
                    self.listAmortization.append(a1)
                else:
                    a = a1 * (1+(self.fees))**(i-1)
                    self.listAmortization.append(round(a,2))
        else:
            for i in range(self.installments+1):
                self.listAmortization.append(0)
        return self.listAmortization

    def balanceDue(self):
        total = self.total
        if self.fees != 0:
            for value in self.listAmortization:
                total -= value
                if total > 0:
                    self.listBalanceDue.append(round(total,2))
                else:
                    self.listBalanceDue.append(0)
        else:
            for i in range(self.installments+1):
                if i == 0:
                    self.listBalanceDue.append(0)
                else:
                    inst = i*self.eachInstallment
                    self.listBalanceDue.append(round((total-inst),2))
        return self.listBalanceDue

    def calculateFees(self):
        for i in range(self.installments+1):
            if self.fees != 0:
                if i == 0:
                    self.listFees.append(0)
                else:
                    currentFee = self.listBalanceDue[i-1] * (self.fees)
                    self.listFees.append(round(currentFee,2))
            else:
                self.listFees.append(0)
        return self.listFees

class simulationInterface():

    sg.theme('LightGrey1')
    
    def __init__(self):
        self.rows=[]
        self.toprow = ['Nº', 'Prestação', 'Juros', 'Amortização', 'Saldo devedor']
        layout = [[sg.Text("Simulação")],
                    [sg.Text("Valor total:"),sg.Input(key='-total')],
                    [sg.Text("Valor de entrada:"),sg.Input(key='-entry')],
                    [sg.Text('Juros:'),sg.Input(key='-fees')],
                    [sg.Text('Número de Prestações:'), sg.Input(key='-installments'), sg.Button('Simular', key='-button')],
                    [sg.Table(values=self.rows,headings=self.toprow,auto_size_columns=True,justification='center',key='-table')],
                    [sg.Button('Gerar PDF', key='-pdf')]]

        self.window = sg.Window("Simulação",layout=layout)

    
    def createInterfaceSimulation(self):
        while True:
            self.event, self.value = self.window.read()
            if self.event == sg.WIN_CLOSED:
                break
            if self.event == '-button':
                self.rows=[]
                self.window['-table'].update(values=self.rows)
                if self.value['-total'] == '':
                    sg.popup('Indicar o valor total',title='ERRO')
                elif self.value['-fees'] == '':
                    sg.popup('Indicar a taxa de juros',title='ERRO')
                elif self.value['-installments'] == '':
                    sg.popup('Indicar o número de prestações', title='ERRO')
                else:
                    if self.value['-entry'] == '':
                        self.value['-entry'] = 0
                    total_value = int(self.value['-total'])
                    entry_value = int(self.value['-entry'])
                    fees_value = float(self.value['-fees'])
                    installments_value = int(self.value['-installments'])
                    simulation = Simulation(total_value,fees_value,entry_value,installments_value)
                    installments = simulation.calculateInstallments()
                    amortization = simulation.amortization()
                    balanceDue = simulation.balanceDue()
                    fees = simulation.calculateFees()
                    for i in range(installments_value+1):
                        row=[]
                        row.append(i)
                        if i == 0:
                            row.append(0)
                        else:
                            row.append(str(installments) + "€")
                        row.append(str(fees[i]) + "€")
                        row.append(str(amortization[i]) + "€")
                        row.append(str(balanceDue[i]) + "€")
                        self.rows.append(row)
                    self.window['-table'].update(values=self.rows)
            if self.event == "-pdf":
                if self.value['-total'] == '':
                    sg.popup('Indicar o valor total',title='ERRO')
                elif self.value['-fees'] == '':
                    sg.popup('Indicar a taxa de juros',title='ERRO')
                elif self.value['-installments'] == '':
                    sg.popup('Indicar o número de prestações', title='ERRO')
                else:
                    if self.value['-entry'] == '':
                        self.value['-entry'] = 0
                    gerar = spdf.SimulationPDF()
                    gerar.conteudo(self.value['-total'],str(self.value['-entry']),self.value['-fees'],self.value['-installments'],self.rows)
                    self.window.close()





