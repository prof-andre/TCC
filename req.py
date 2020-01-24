import requests as rt
import pandas as pd
import numpy as np
import PyPDF2 as p2
from pathlib import Path
import os

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

def download_pdf_ano(ano, path):
#Faz o download de todos os aquivos do ano informado, verifica a se há erro na escrita de cada arquivo e exclui os arquivos errados.

    end_V = []
    end_F = []
    COD_V = []
    COD = trans_csv(path)
    for x in COD:
        end_pdf = download_pdf(ano, x)
        prop = os.stat(end_pdf)
        if prop.st_size == 1245:
            end_F.append(end_pdf)
            os.remove(end_pdf)
        else:
            end_V.append(end_pdf)
            COD_V.append(COD)
    
    for x in range(len(end_F),len(end_V)):
        end_F.append('')
    data = {'END_TRUE': end_V, 'END_FALSE': end_F}
    frame = pd.DataFrame(data)
    csv = frame.to_csv('NOME_ARQUIVOS_' + str(ano) + '.csv')
    return end_V

def le_pdf(path):
#Recebe o caminho do arquivo pdf e retorna um dict(key=Nº, value=conteúdo da página).

    arq = open(path, "rb")
    pdf = p2.PdfFileReader(arq)
    pg_pdf = {}
    for i in range(0, pdf.getNumPages()):        
        pg_pdf[i+1] = [pdf.getPage(i).extractText()]
        
    arq.close()
    return pg_pdf

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

def __array_dados(pg_pdf, pg):
#recebe um dict com a leitura primaria do pdf e retorna uma array somente com os valores na forma de strings.
    dados = []
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
    return dados

def monta_banco(_array_, ANO, cod):
#para 2018, 2017,2016_m_f,2015_m_f,2014_m_f no 3ano
    _array_num_f = []
    _array_num_m = []
    _array_ano = []
    _array_cod = []
#IF -> Indicadores do Fundamental
#IM -> Indicadores do Médio
#COD -> Codigo da escola

    if len(_array_) <= 22:
        for i in range(0,5):
            _array_num_m.append(float(_array_[i].replace(',','.')))
            _array_ano.append(int(ANO))
            _array_cod.append(cod)
        data = {'IM':_array_num_m,'ANO':_array_ano,'COD':_array_cod}
    else:
        for i in range(0,10):
            if i <= 4:
                _array_num_f.append(float(_array_[i].replace(',','.')))
                _array_ano.append(int(ANO))
                _array_cod.append(cod)
            else:
                _array_num_m.append(float(_array_[i].replace(',','.')))
        data = {'IF':_array_num_f,'IM':_array_num_m,
'ANO':_array_ano,'COD':_array_cod}

#P -> Português
#M -> Matemática
#DH -> Desempenho
#FX -> Fluxo
#NI -> Nota IDESP
    frame = pd.DataFrame(data, columns = ['IM','IF','ANO','COD'], index = ['P','M','DH','FX','NI']) 

    return frame
