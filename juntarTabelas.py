import sqlite3

# Caminho para os bancos de dados
caminho_db_x = 'pontos.db'
caminho_db_y = 'siteSB/my_database.db'
nome_tabela = 'ponibus'

# Conectar ao banco de dados X
conexao_x = sqlite3.connect(caminho_db_x)
cursor_x = conexao_x.cursor()

# Conectar ao banco de dados Y
conexao_y = sqlite3.connect(caminho_db_y)
cursor_y = conexao_y.cursor()

# Obter o comando CREATE TABLE da tabela no banco de dados X
cursor_x.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'")
result = cursor_x.fetchone()

if result is None:
    print(f"Tabela '{nome_tabela}' não encontrada no banco de dados X.")
else:
    create_table_sql = result[0]

    # Criar a tabela no banco de dados Y
    cursor_y.execute(create_table_sql)

    # Obter todos os dados da tabela no banco de dados X
    cursor_x.execute(f"SELECT * FROM {nome_tabela}")
    dados = cursor_x.fetchall()

    # Obter o número de colunas da tabela
    num_colunas = len(cursor_x.description)

    # Criar um placeholder para os valores (e.g., ?, ?, ?)
    placeholders = ', '.join(['?'] * num_colunas)

    # Inserir os dados no banco de dados Y
    cursor_y.executemany(f"INSERT INTO {nome_tabela} VALUES ({placeholders})", dados)

    # Confirmar as mudanças no banco de dados Y
    conexao_y.commit()

# Fechar as conexões
conexao_x.close()
conexao_y.close()
