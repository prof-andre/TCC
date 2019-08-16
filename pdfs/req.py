import requests as rt
import pandas as pd
import numpy as np
import PyPDF2 as p2
from pathlib import Path

def trans_csv(path):
#Recebe o caminho do arquivo csv e retorna uma array do tipo string. Leitura do arquivo csv com os dados das escolas. Transforma a coluna COD_ESC em uma unida Array do tipo string.

    data = pd.read_csv(path)
    cod_n = np.array(data['COD_ESC'])
    cod_s = []
    for x in cod_n:
        x = str(x)
        if len(x) < 6: 
            cod_s.append('0'*(6-len(x)) + str(x))
        else:
            cod_s.append(x)
    return cod_s

def download_pdf(ano, COD_ESC):
#Recebe ano como inteiro e COD_ESC como string para determinar o  endereço do arquivo e definição do nome para ser salvo. Retorna o nome do arquivo.

    ano = str(ano)
    url = 'http://idesp.edunet.sp.gov.br/arquivos' + ano + '/' + COD_ESC + '.pdf'
    end_pdf = ano + '_' + COD_ESC + '.pdf'

    response = rt.get(url)
    filename = Path(end_pdf)
    filename.write_bytes(response.content)
    print(url)
    return end_pdf

def le_pdf(path):
#Recebe o caminho do arquivo pdf e retorna um dict(key=Nº, value=conteúdo da página).

    arq = open(path, "rb")
    pdf = p2.PdfFileReader(arq)
    pg_pdf = {}
    for i in range(0, pdf.getNumPages()):        
        pg_pdf[i+1] = [pdf.getPage(i).extractText()]
        
    arq.close()
    return pg_pdf

def PD_2007(pg_pdf,pg):
    dados = []
    for i in range(0, len(pg_pdf[pg][0])):
        if pg_pdf[pg][0][i] == ',':
            dados.append(float(pg_pdf[pg][0][i-1]+'.'+pg_pdf[pg][0][i+1]+pg_pdf[pg][0][i+2]))
    return dados

def PD_novo(pg_pdf, pg):
#serve para 2013 para frente
    dados = []
    num_dados = []
    start = 0
    first = True
    for i in range(0, len(pg_pdf[pg][0])):
        if pg_pdf[pg][0][i] == '\n' and first:            
            dados.append(str(pg_pdf[pg][0][0:i]))
            start = i+1
            first = False
        elif pg_pdf[pg][0][i] == '\n':
            dados.append(str(pg_pdf[pg][0][start:i]))
            start = i+1
    for i in range(0,len(dados)):
        num_dados.append(float(dados[i].replace(',','.')))
    return num_dados
