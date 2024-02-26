from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date
import os

def drawPageFrame(canvas, doc):
    canvas.saveState()
    canvas.drawImage(os.path.dirname(__file__)+"/watermark.png",49,167.88)
    canvas.restoreState()


class ReceiptsPDF():
    
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        dir = self.dir + "/Recibos"
        initial_count = 0
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)):
                initial_count += 1

        self.file_name = dir + "/Recibo" + str(initial_count) + ".pdf"

        self.largura = 595.27
        self.altura = 841.89

        self.c = SimpleDocTemplate(self.file_name, pagesize=(self.largura, self.altura))
        self.story = []

    def conteudo(self, nome, nif, valor, marca, modelo, matricula):

        self.story.append(Spacer(1,40))

        imagem_path = self.dir + "/logo3.png"
        imagem = Image(imagem_path, width=140, height=43, hAlign="LEFT")
        self.story.append(imagem)
        
        self.story.append(Spacer(1,40))

        styles = getSampleStyleSheet()
        titulo = Paragraph("Recibo",styles['Title'])
        self.story.append(titulo)

        self.story.append(Spacer(1,50))

        text = f"""Rafael Zebende de Moraes, NIF 299217990, declara que recebeu de {nome}, NIF {nif}, a quantia de {valor}€ 
         referente à entrada correspondente à aquisição do automóvel {marca} {modelo}, com matrícula {matricula}. """

        self.story.append(Paragraph(text, styles['Normal']))

        self.story.append(Spacer(1,20))

        data = (date.today()).strftime('%d/%B/%Y')
        dia, mes, ano = data.split("/")

        if mes == "January":
            mes = "janeiro"
        elif mes == "February":
            mes = "fevereiro"
        elif mes == "March":
            mes = "março"
        elif mes == "April":
            mes = "abril"
        elif mes == "May":
            mes = "maio"
        elif mes == "June":
            mes = "junho"
        elif mes == "July":
            mes = "julho"
        elif mes == "August":
            mes = "agosto"
        elif mes == "September":
            mes = "setembro"
        elif mes == "October":
            mes = "outubro"
        elif mes == "November":
            mes = "novembro"
        else:
             mes = "dezembro"

        self.story.append(Paragraph(f"Braga, {dia} de {mes} de {ano} ", styles['Normal']))

        self.story.append(Spacer(1,40))

        self.story.append(Paragraph("____________________________________________", styles['Normal']))
        self.story.append(Paragraph("                 Assinatura                 ", styles['Normal']))

        self.story.append(Spacer(1,25))
        
        self.story.append(Paragraph("____________________________________________", styles['Normal']))
        self.story.append(Paragraph("                 Assinatura                 ", styles['Normal']))

        self.c.build(self.story,onFirstPage=drawPageFrame,onLaterPages=drawPageFrame)

