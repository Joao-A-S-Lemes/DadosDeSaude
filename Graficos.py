import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




def graficos():
    #Carregar dados
    try:
        dados = pd.read_csv('Data/Atividade2Revisada.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return
    else:
        print("Arquivo encontrado")


    #GRAFICO 1
    #Filtrar apenas as pessoas que tiveram AVC (stroke = 1)
    stroke_dados = dados[dados['stroke'] == 1].copy()

    #Definir faixas etárias para agrupar os dados
    bins = [0, 50, 60, 70, 80, 120]
    labels = ['Até 50 anos', '51 a 60 anos', '61 a 70 anos', '71 a 80 anos', '80 anos ou mais']

    stroke_dados['faixa_etaria'] = pd.cut(stroke_dados['age'], bins=bins, labels=labels, right=True)
    counts = stroke_dados['faixa_etaria'].value_counts().sort_index()

    #Configurar e gerar o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'],
        wedgeprops={'edgecolor': 'black'}
    )

    plt.title('Distribuição Percentual de Pessoas que Tiveram AVC por Faixa Etária', fontsize=14, fontweight='bold',
              pad=20)
    plt.tight_layout()

    # Salvar e exibir o gráfico
    plt.savefig('Data/grafico1.png', dpi=300)
    plt.show()

    #GRAFICO 2
    cross_tab = pd.crosstab(dados['stroke'], dados['hypertension'], normalize='index') * 100

    # Plotar gráfico de barras empilhadas
    ax = cross_tab.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#aec7e8', '#ff7f0e'])

    plt.title('Proporção de Hipertensão em Pessoas com e sem AVC (%)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Histórico de AVC', fontsize=11)
    plt.ylabel('Porcentagem (%)', fontsize=11)
    plt.xticks(ticks=[0, 1], labels=['Sem AVC', 'Com AVC'], rotation=0)
    plt.legend(title='Hipertensão', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adicionar os rótulos de porcentagem nas barras
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='center')

    plt.tight_layout()
    plt.savefig('Data/grafico2.png', dpi=300)
    plt.show()

