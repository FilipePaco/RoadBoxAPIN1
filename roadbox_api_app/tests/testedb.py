import mysql.connector  # Usando MariaDB
from datetime import datetime

# Configuração para conexão com o banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='roadbox_ubiquo',
    port=3306,
    charset='utf8mb4',  # Definindo o charset
    collation='utf8mb4_general_ci'  # Definindo uma collation compatível
)

cursor = conn.cursor()

# Dados de teste
dispositivo = 'Dispositivo_Teste_Inserção_teste'
foto_sinistro = 'https://drive.google.com/file/d/1pf5dooUDiYFDWhUhWWtNbOUWpxl-3Vja/view?usp=sharing'
data_hora = datetime.now()
latitude = -16.6809
longitude = -49.2536

# Inserindo os dados no banco de dados
try:
    cursor.execute('''
        INSERT INTO enviodesinistro (dispositivo, foto_sinistro, data_hora, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    ''', (dispositivo, foto_sinistro, data_hora, latitude, longitude))
    conn.commit()
    print("Dados inseridos com sucesso.")
except mysql.connector.Error as err:
    print(f"Erro ao inserir os dados: {err}")
finally:
    # Fecha a conexão com o banco após uso
    cursor.close()
    conn.close()
