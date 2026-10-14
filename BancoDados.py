import sqlite3
import pandas as pd

def criar_banco():
    #Carregar dados tratados
    try:
        dados = pd.read_csv('Data/Atividade2Revisada.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado")
        return
    else:
        print("\nCriando banco de dados SQLite...")

    #Traduzir as categorias de gênero e tabagismo
    dados['gender'] = dados['gender'].replace({'Male': 'Masculino', 'Female': 'Feminino', 'Other': 'Outro'})
    dados['smoking_status'] = dados['smoking_status'].replace({
        'Unknown': 'Desconhecido',
        'formerly smoked': 'Ex-fumante',
        'never smoked': 'Nunca fumou',
        'smokes': 'Fumante'
    })

    #Criar o banco e a tabela
    conexao = sqlite3.connect('Data/saude.db')
    cursor = conexao.cursor()

    cursor.execute('DROP TABLE IF EXISTS pacientes')
    cursor.execute('''
        CREATE TABLE pacientes (
            id INTEGER PRIMARY KEY,
            genero TEXT,
            idade REAL,
            hipertensao INTEGER,
            doenca_cardiaca INTEGER,
            casado TEXT,
            tipo_trabalho TEXT,
            tipo_residencia TEXT,
            glicose REAL,
            imc REAL,
            tabagismo TEXT,
            avc INTEGER
        )
    ''')

    #Inserir os dados tratados
    registros = list(dados.itertuples(index=False, name=None))
    cursor.executemany('INSERT INTO pacientes VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', registros)
    conexao.commit()

    #CONSULTA 1: quantidade total de registros
    cursor.execute('SELECT COUNT(*) FROM pacientes')
    print(f"\nConsulta 1 - Total de registros: {cursor.fetchone()[0]}")

    #CONSULTA 2: pacientes com registro de AVC
    cursor.execute('SELECT id, genero, idade, hipertensao, doenca_cardiaca, glicose, imc, tabagismo '
                   'FROM pacientes WHERE avc = 1')
    com_avc = cursor.fetchall()
    print(f"\nConsulta 2 - Pacientes com AVC: {len(com_avc)} (mostrando os 10 primeiros)")
    for linha in com_avc[:10]:
        print(linha)

    #CONSULTA 3: média de glicose e IMC por grupo (com e sem AVC)
    cursor.execute('SELECT avc, COUNT(*), ROUND(AVG(glicose), 2), ROUND(AVG(imc), 2) '
                   'FROM pacientes GROUP BY avc')
    print("\nConsulta 3 - Glicose e IMC médios por grupo (avc, qtd, glicose, imc):")
    for linha in cursor.fetchall():
        print(linha)

    conexao.close()