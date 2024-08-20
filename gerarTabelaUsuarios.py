import sqlite3
import os

# Caminho absoluto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'PCD.db')

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Criar a tabela users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL
)
''')

# Inserir dados de exemplo (opcional)
c.execute('''
INSERT INTO users (cpf, senha, nome) VALUES
('12345678900', 'SIGA BEM', 'Artur')
''')

# Salvar (commit) as mudanças e fechar a conexão
conn.commit()
conn.close()