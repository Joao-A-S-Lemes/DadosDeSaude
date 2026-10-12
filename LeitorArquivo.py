import pandas as pd
from datetime import datetime

def tratar_dados():
    #carregar o arquivo
    try:
        data = pd.read_csv('Data/Atividade2.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado")
    else:
        print("Arquivo encontrado")
    #Quantidade de linhas originais
    linhas_originais = data.shape[0]
    #quantidade de colunas originais
    colunas_originais = data.shape[1]
    #Nomes das colunas
    colunas = data.columns.tolist()

    #Verificar dados ausentes
    ausentes = data.isnull().sum()
    total_ausentes = ausentes.sum()


    print(linhas_originais)
    print(colunas_originais)
    print(colunas)
