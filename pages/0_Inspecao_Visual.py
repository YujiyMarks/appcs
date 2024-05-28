
import streamlit as st #biblioteca para a parte visual

# bibliotecas para gerar o pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, LongTable, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

styles = getSampleStyleSheet() # estilos dos paragrafos

from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]

import io

#conexão com o banco de dados
import sqlite3

dados = sqlite3.connect('bd_app.db')
cursor = dados.cursor()


# definição do modelo da capa
def capa(canvas, doc): 
    canvas.setAuthor("BrunoY")
    canvas.setTitle("Relatorio")

    canvas.drawImage("cs.png", PAGE_WIDTH/2.0-85, PAGE_HEIGHT-170, width=200,height=80) 

    canvas.bookmarkPage("capa") 
    canvas.addOutlineEntry("Capa","capa")

    canvas.setFont('Times-Roman',11)
    canvas.drawString(1.5*inch, 1.5 * inch, "Legenda: C - Conforme / NC - Não Conforme / NA - Não Aplicável / PA - Ponto de Atenção")
    
    canvas.line(10,140,PAGE_WIDTH,140) 
    canvas.setFont('Times-Roman',8)
    #canvas.drawString(inch, 0.9*inch, "Page %d" % (doc.page))  
    canvas.drawString(2.5*inch, 1*inch, "Canal Solar - Consultoria & Serviços | Departamento de Engenharia")
    canvas.drawString(2.5*inch, 0.85*inch, "R. Paulo César Fidélis, - Lot. Res. Vila Bella, Campinas - SP, 13087-727")
    canvas.drawString(2.5*inch, 0.7*inch, "engenharia@canalsolar.com.br | canalsolar.com.br")
    canvas.drawString(2.5*inch, 0.55*inch, "(19)99605-9172 | (19) 99899-7915") 


# definição do modelo das outras paginas
def paginas(canvas, doc):
     canvas.drawImage("cs.png", PAGE_WIDTH-100, PAGE_HEIGHT-100, width=100,height=50)

     canvas.setFont('Times-Roman',8)
     canvas.drawString(inch, 0.75*inch, "Page %d" % (doc.page))  
     canvas.drawString(2.5*inch, 0.70*inch, "Canal Solar - Consultoria & Serviços | Departamento de Engenharia")
     canvas.drawString(2.5*inch, 0.55*inch, "R. Paulo César Fidélis, - Lot. Res. Vila Bella, Campinas - SP, 13087-727")
     canvas.drawString(2.5*inch, 0.40*inch, "engenharia@canalsolar.com.br | canalsolar.com.br")
     canvas.drawString(2.5*inch, 0.25*inch, "(19)99605-9172 | (19) 99899-7915") 


# função para gerar o pdf
def gerar_pdf(ufv,cliente,img,inspetor,revisor,data,num_items,itens,imagens,imagens2,analises,obs):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,leftMargin=inch,rightMargin=inch,
                    topMargin=inch,bottomMargin=inch,title='Relatorio',author='BrunoY')
    relatorio = []

    #definição dos estilos
    titulo_estilo = styles['Heading2']
    subtitulo_estilo = styles['Heading4']
    conteudo_estilo = ParagraphStyle('normal', fontName='Helvetica', fontSize=10, alignment=TA_CENTER)
    capa_estilo = ParagraphStyle('normal', fontName='Helvetica', fontSize=20, alignment=TA_CENTER)


    # seção da capa
    relatorio.append(Spacer(1,70))

    relatorio.append(Paragraph(f"UFV {ufv} - {cliente}",capa_estilo))
    relatorio.append(Spacer(1,50))

    #relatorio.append(Paragraph(f"{cliente}",capa_estilo))
    #relatorio.append(Spacer(1,30))

    relatorio.append(Paragraph(f"Imagem Geral",conteudo_estilo))
    relatorio.append(Spacer(1,15))
    img_ger = Image(img, width=340,height=190)
    imagem_geral = [[img_ger]]
    imagem_capa = Table(imagem_geral, colWidths=350, rowHeights=200) 
    imagem_capa.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('ALIGN',(1,1),(-3,-3),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(1,-1),colors.black),('FONTSIZE', (0,0), (-1,-1), 12)]))
    relatorio.append(imagem_capa)
    relatorio.append(Spacer(1,50))

    relatorio.append(Paragraph("Relatório de Inspeção Visual",capa_estilo))
    relatorio.append(Spacer(1,30))

    dados_tabela = [["Inspetor", inspetor],["Revisor",revisor],["Responsável","Bruno Kikumoto"]]
    tabela_capa = Table(dados_tabela, colWidths=175, rowHeights=30) 
    tabela_capa.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('ALIGN',(1,1),(-3,-3),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(1,-1),colors.black),('FONTSIZE', (0,0), (-1,-1), 12)]))
    relatorio.append(tabela_capa)

    relatorio.append(Spacer(1,30))
    relatorio.append(Paragraph(f"Data de Elaboração: {data}"))


    # seção dos itens
    relatorio.append(PageBreak())

    titulo = Paragraph("RESULTADOS OBTIDOS", capa_estilo)
    relatorio.append(titulo)
    relatorio.append(Spacer(1,30))

    for i in range(num_items):
        dados_itens = [[f"Item {i+1} - {itens[i]}"]]
        tabela_itens = Table(dados_itens, colWidths=350, rowHeights=30) 
        tabela_itens.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('ALIGN',(1,1),(-3,-3),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(1,-1),colors.black),('FONTSIZE', (0,0), (-1,-1), 12)]))
        relatorio.append(tabela_itens)

        img_item = Image(imagens[i], width=340,height=190)
        dados_itens = [[img_item]]
        tabela_itens = Table(dados_itens, colWidths=350, rowHeights=200) 
        tabela_itens.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('ALIGN',(1,1),(-3,-3),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(1,-1),colors.black),('FONTSIZE', (0,0), (-1,-1), 12)]))
        relatorio.append(tabela_itens)

        img2_item = Image(imagens2[i], width=340,height=190)
        dados_itens = [[img2_item]]
        tabela_itens = Table(dados_itens, colWidths=350, rowHeights=200) 
        tabela_itens.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('ALIGN',(1,1),(-3,-3),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(1,-1),colors.black),('FONTSIZE', (0,0), (-1,-1), 12)]))
        relatorio.append(tabela_itens)

        dados_itens = [[f"Análise: {analises[i]}"],[f"Observação: {obs[i]}"]]
        tabela_itens = Table(dados_itens, colWidths=350, rowHeights=30) 
        tabela_itens.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('ALIGN',(1,1),(-3,-3),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,0),(1,-1),colors.black),('FONTSIZE', (0,0), (-1,-1), 12)]))
        relatorio.append(tabela_itens)

        relatorio.append(PageBreak())
        #if i < num_items-1:
        #    relatorio.append(Spacer(1,50))

    doc.build(relatorio, onFirstPage=capa, onLaterPages=paginas)
    st.success("Relatório gerado com sucesso!")
    st.download_button(label="Baixar PDF", data=buffer.getvalue(), file_name=f"relatorio_inspecao.pdf", mime="application/pdf")
    


# criação da tela de relatório
def main():
    # configurações iniciais
    st.set_page_config(page_title="Relatorio CS",page_icon="page_facing_up:",)
    st.sidebar.header("Inspeção Visual")

    st.title("Relatório de Inspeção Visual")

    # inserção dos campos para recebimento dos valores do banco de dados
    cursor.execute("SELECT * FROM Usinas")
    lista = []
    for linha in cursor.fetchall():
        lista.append(linha[1])
    ufv = st.selectbox("UFV:",lista)

    cursor.execute("SELECT * FROM Clientes")
    lista = []
    for linha in cursor.fetchall():
        lista.append(linha[1])
    cliente = st.selectbox("Cliente",lista)

    cursor.execute("SELECT * FROM Funcionarios")
    lista = []
    for linha in cursor.fetchall():
        lista.append(linha[1])
    inspetor = st.selectbox("Responsável",lista)
    revisor = st.selectbox("Revisor",lista)
    
    data = st.date_input("Data de elaboração:")
    img = st.file_uploader("Imagem geral:")


    # inserção dos campos para recebimento dos itens
    st.header("ITENS")
    # botão para escolha da quantidade de itens
    num_items = st.number_input("Número de itens:", min_value=1, step=1, value=1)

    itens = []
    imagens = []
    imagens2 = []
    analises = []
    obs = []
    # inserção dos campos dos itens de acordo com o número de itens
    for i in range(num_items):
        st.subheader(f"Item {i+1}")
        cursor.execute("SELECT * FROM Equipamentos")
        lista = []
        for linha in cursor.fetchall():
            lista.append(linha[1])
        item = st.selectbox(f"Escolha o item {i+1}:",lista)
        itens.append(item)
        imagem = st.file_uploader(f"Insira a 1º imagem do item {i+1}:",type=['jpg','png'])
        imagens.append(imagem)
        imagem2 = st.file_uploader(f"Insira a 2º imagem do item {i+1}:",type=['jpg','png'])
        imagens2.append(imagem2)
        analise = st.radio(f"Análise do item {i+1}:",["C","NC","NA","PA"],horizontal=True)
        analises.append(analise)
        observacao = st.text_input(f"Digite a observação do item {i+1}:")
        obs.append(observacao)

    # botão para geração do relatório
    if st.button("Gerar Relatório"):
        if itens:   
            gerar_pdf(ufv,cliente,img,inspetor,revisor,data,num_items,itens,imagens,imagens2,analises,obs)
        else:
            st.warning("Erro ao gerar o PDF.")


if __name__ == "__main__":
    main()
