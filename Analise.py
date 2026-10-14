import pandas as pd

def analisar():
    #Mostrar todas as colunas nos prints
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)

    #Carregar dados tratados
    try:
        dados = pd.read_csv('Data/Atividade2Revisada.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return
    else:
        print("\nIniciando análise dos dados...")

    #Traduzir os nomes das colunas para português para melhor entendimento
    dados = dados.rename(columns={
        'stroke': 'avc',
        'age': 'idade',
        'avg_glucose_level': 'glicose',
        'bmi': 'imc',
        'hypertension': 'hipertensao',
        'heart_disease': 'doenca_cardiaca',
        'smoking_status': 'tabagismo'
    })

    #Traduzir as categorias de tabagismo
    dados['tabagismo'] = dados['tabagismo'].replace({
        'Unknown': 'Desconhecido',
        'formerly smoked': 'Ex-fumante',
        'never smoked': 'Nunca fumou',
        'smokes': 'Fumante'
    })

    print("\nDados carregados! Resultados a caminho...")

    #Separar os grupos (filtros)
    com_avc = dados[dados['avc'] == 1]
    sem_avc = dados[dados['avc'] == 0]

    print("\n=== TAMANHO DOS GRUPOS ===")
    print(f"Com AVC: {len(com_avc)}")
    print(f"Sem AVC: {len(sem_avc)}")
    print(f"Taxa geral de AVC: {len(com_avc) / len(dados) * 100:.2f}%")

    #Estatísticas das variáveis numéricas por grupo (agrupamento)
    print("\n=== IDADE, GLICOSE E IMC POR GRUPO ===")
    for variavel in ['idade', 'glicose', 'imc']:
        resumo = dados.groupby('avc')[variavel].agg(['mean', 'median', 'std']).round(2)

        #Traduzir os nomes das colunas e dos grupos
        resumo.columns = ['media', 'mediana', 'desvio_padrao']
        resumo.index = ['Sem AVC', 'Com AVC']

        print(f"\n{variavel.upper()}")
        print(resumo.to_string(float_format='%.2f'))

    #Porcentagem de hipertensos e cardíacos em cada grupo
    print("\n=== HIPERTENSÃO E DOENÇA CARDÍACA (% em cada grupo) ===")
    for coluna in ['hipertensao', 'doenca_cardiaca']:
        porcentagens = (dados.groupby('avc')[coluna].mean() * 100).round(2)
        print(f"{coluna}:")
        print(f"  Sem AVC: {porcentagens[0]}%")
        print(f"  Com AVC: {porcentagens[1]}%")

    #Tabagismo em cada grupo
    print("\n=== TABAGISMO (% dentro de cada grupo) ===")
    print((pd.crosstab(dados['avc'], dados['tabagismo'], normalize='index') * 100).round(2))

    #Taxa de AVC por faixa etária
    print("\n=== TAXA DE AVC POR FAIXA ETÁRIA (%) ===")
    dados['faixa_etaria'] = pd.cut(dados['idade'], bins=[0, 40, 60, 80, 120],
                                   labels=['Até 40', '41 a 60', '61 a 80', 'Mais de 80'])
    taxas = (dados.groupby('faixa_etaria', observed=True)['avc'].mean() * 100).round(2)
    for faixa, taxa in taxas.items():
        print(f"{faixa}: {taxa:.2f}%")