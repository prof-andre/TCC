import requests as rt
import csv
from pathlib import Path

#leitura do arquivo csv com os dados das escolas
with open('escola.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    cabecalho = True
    for row in csv_reader:
        if cabecalho:
            print(f'Nomes: {",".join(row)}')
            cabecalho = False
        else:
            print(f'{",".join(row)}')

#baixar pdfs com os dados
filename = Path('/home/andre/Área de Trabalho/04.pdf')
url = 'http://idesp.edunet.sp.gov.br/arquivos2018/044349.pdf'
response = requests.get(url)
filename.write_bytes(response.content)


