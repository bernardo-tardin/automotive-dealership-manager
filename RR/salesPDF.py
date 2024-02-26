from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def drawPageFrame(canvas, doc):
    canvas.saveState()
    canvas.drawImage(os.path.dirname(__file__)+"/watermark.png",49,167.88)
    canvas.restoreState()

class SalesPDF():
    
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        dir = self.dir + "/Vendas"
        initial_count = 0
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)):
                initial_count += 1

        self.file_name = dir + "/venda" + str(initial_count) + ".pdf"

        self.largura = 595.27
        self.altura = 841.89

        self.c = SimpleDocTemplate(self.file_name, pagesize=(self.largura, self.altura))
        self.story = []

    def conteudo(self, nome, nif, telefone, email, morada, localidade, codigo_postal, identificacao, matricula, marca, modelo, ano,valor_total, valor_entrada, prestacoes,table):

        imagem_path = self.dir + "/logo3.png"
        imagem = Image(imagem_path, width=140, height=43, hAlign="LEFT")
        self.story.append(imagem)
        
        self.story.append(Spacer(1,40))

        styles = getSampleStyleSheet()
        titulo = Paragraph("Venda de Automóvel",styles['Title'])
        self.story.append(titulo)

        self.story.append(Spacer(1,30))

        self.story.append(Paragraph("Comprador",styles['Heading3']))
        self.story.append(Paragraph(f'Nome: {nome}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Telemóvel: {telefone}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Email: {email}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Morada: {morada}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Localidade: {localidade}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Código Postal: {codigo_postal}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'NIF: {nif}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'{identificacao}',styles['Normal']))

        self.story.append(Spacer(1,12))

        self.story.append(Paragraph("Automóvel",styles['Heading3']))
        self.story.append(Paragraph(f'Matrícula: {matricula}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Marca: {marca}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Modelo: {modelo}',styles['Normal']))
        self.story.append(Spacer(1,8))
        self.story.append(Paragraph(f'Ano: {ano}',styles['Normal']))
        self.story.append(Spacer(1,8))

        self.story.append(Spacer(1,12))

        self.story.append(Paragraph("Condições",styles['Heading3']))
        
        total_value = "Valor total: " + valor_total + "€"
        entry_value = "Valor de entrada: " + valor_entrada + "€"
        n_installments = "Número de prestações: " + prestacoes

        self.texto_lista = [
            total_value,
            entry_value,
            n_installments]
        
        for item in self.texto_lista:
            self.story.append(Paragraph(f"{item}", styles['Normal']))
            self.story.append(Spacer(1,8))

        self.story.append(Spacer(1,30))
        
        self.story.append(Paragraph("____________________________________________", styles['Normal']))
        self.story.append(Paragraph("                 Assinatura                 ", styles['Normal']))

        self.story.append(Spacer(1,25))
        
        self.story.append(Paragraph("____________________________________________", styles['Normal']))
        self.story.append(Paragraph("                 Assinatura                 ", styles['Normal']))

        self.story.append(Spacer(1,60))

        self.dados_tabela = [["Nº da Prestação", "Data de Vencimento", "Valor (€)"]]

        for row in table:
            self.dados_tabela.append(row[0:len(row)-1])
        
        self.tabela =  Table(self.dados_tabela, cornerRadii=(4,4,4,4))

        self.estilo = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                         ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                         ('GRID', (0, 0), (-1, -1), 1, colors.black),
                         ('VALIGN', (0, 0),(-1,-1),'MIDDLE')])

        self.tabela.setStyle(self.estilo)
        self.story.append(self.tabela)

        self.c.build(self.story,onFirstPage=drawPageFrame,onLaterPages=drawPageFrame)

