import pandas as pd
import matplotlib.pyplot as plt

def graficos():
    #Carregar dados
    try:
        dados = pd.read_csv('Data/Atividade2Revisada.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return
    else:
        print("\nGerando gráficos...")

    #GRAFICO 1
    #Filtrar apenas as pessoas que tiveram AVC (stroke = 1)
    stroke_dados = dados[dados['stroke'] == 1].copy()

    #Configurar e gerar o histograma das idades
    plt.figure(figsize=(8, 6))
    plt.hist(stroke_dados['age'], bins=10, color='#66b3ff', edgecolor='black')

    #Título e identificação dos eixos
    plt.title('Distribuição das Idades dos Pacientes com AVC', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Idade (anos)', fontsize=11)
    plt.ylabel('Número de pacientes', fontsize=11)
    plt.tight_layout()

    #Salvar o gráfico
    plt.savefig('Data/grafico1.png', dpi=300)
    plt.close()

    #GRAFICO 2
    cross_tab = pd.crosstab(dados['stroke'], dados['hypertension'], normalize='index') * 100

    #Plotar gráfico de barras empilhadas
    ax = cross_tab.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#aec7e8', '#ff7f0e'])

    plt.title('Proporção de Hipertensão em Pessoas com e sem AVC (%)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Histórico de AVC', fontsize=11)
    plt.ylabel('Porcentagem (%)', fontsize=11)
    plt.xticks(ticks=[0, 1], labels=['Sem AVC', 'Com AVC'], rotation=0)
    plt.legend(title='Hipertensão', bbox_to_anchor=(1.05, 1), loc='upper left')

    #Adicionar os rótulos de porcentagem nas barras
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', label_type='center')

    plt.tight_layout()
    plt.savefig('Data/grafico2.png', dpi=300)
    plt.close()

    #GRAFICO 3
    #Definir faixas etárias para agrupar os pacientes
    bins = [0, 40, 60, 80, 120]
    labels = ['Até 40', '41 a 60', '61 a 80', 'Mais de 80']
    dados['faixa_etaria'] = pd.cut(dados['age'], bins=bins, labels=labels)

    #Calcular a taxa de AVC (%) em cada faixa etária
    taxa = dados.groupby('faixa_etaria', observed=True)['stroke'].mean() * 100

    #Configurar e gerar o gráfico de barras
    plt.figure(figsize=(8, 6))
    barras = plt.bar(taxa.index, taxa.values, color='#ff7f0e', edgecolor='black')
    plt.bar_label(barras, fmt='%.1f%%')

    #Título e identificação dos eixos
    plt.title('Taxa de AVC por Faixa Etária (%)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Faixa etária (anos)', fontsize=11)
    plt.ylabel('Pacientes com AVC (%)', fontsize=11)
    plt.tight_layout()

    #Salvar o gráfico
    plt.savefig('Data/grafico3.png', dpi=300)
    plt.close()