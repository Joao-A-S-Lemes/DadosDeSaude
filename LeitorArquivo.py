import pandas as pd
from datetime import datetime

def tratar_dados():
    #Carregador do aquivo
    try:
        data = pd.read_csv('Data/Atividade2.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado")
    else:
        print("Arquivo encontrado")

    #Quantidade de linhas originais
    linhas_originais = data.shape[0]

    #Quantidade de colunas originais
    colunas_originais = data.shape[1]

    #Nomes das colunas
    colunas = data.columns.tolist()

    #Verifica dados ausentes
    ausentes = data.isnull().sum()
    total_ausentes = ausentes.sum()

    #Remove linhas vazias
    data.dropna(how='all', inplace=True)

    #Preenche números ausentes com mediana
    numeros_null = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeros_null:
        data[col] = data[col].fillna(data[col].median())

    #Substituir dados de texto null por N/A
    texto_null = data.select_dtypes(include=['object']).columns
    for col in texto_null:
        data[col] = data[col].fillna("N/A")

    #Evidências após tratamento
    ausentes_depois = data.isnull().sum()
    total_ausentes_depois = ausentes_depois.sum()
    registros_finais = data.shape[0]

    #Salva a nova base de dados
    data.to_csv("Data/Atividade2Revisada.csv", index=False)

    #Data e hora da verificação
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Relatório
    relatorio_evidencias = (
        f"Data da execução: {data_hora}\n"
        f"Base original: {"Data/Atividade2.csv"}\n"
        f"Base tratada gerada: {"Data/Atividade2Revisada.csv"}\n"
        f"\n"
        f"1 - ANÁLISE INICIAL\n"
        f"- Total de características (colunas): {colunas_originais}\n"
        f"- Nomes das colunas: {', '.join(colunas)}\n"
        f"- Total de registros (linhas): {linhas_originais}\n"
        f"- Total de dados ausentes encontrados: {ausentes}\n\n"
        f"2 - TRATAMENTO APLICADO\n"
        f"- Linhas 100% vazias foram removidas.\n"
        f"- Colunas numéricas preenchidas com a mediana.\n"
        f"- Colunas de texto preenchidas com a string 'N/A'.\n\n"
        f"3 - VALIDAÇÃO E EVIDÊNCIAS (PÓS-TRATAMENTO)\n"
        f"- Registros finais processados: {registros_finais}\n"
        f"- Dados ausentes restantes: {total_ausentes_depois} (Prova de tratamento eficaz)\n"
        f"- Status final por coluna:\n{ausentes_depois.to_string()}\n"
        f"========================================\n"
    )

    #Escrevce o relatório para comprovação
    with open("Data/evidencia.txt", 'w', encoding='utf-8') as f:
        f.write(relatorio_evidencias)

    print(f"Concluído! A base limpa foi salva em '{"Data/Atividade2Revisada.csv"}'.")
    print(f"As evidências do tratamento foram geradas no arquivo '{"Data/evidencia.txt"}'.")