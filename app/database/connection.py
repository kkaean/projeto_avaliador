import mysql.connector
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

def get_connection():
    """
    Estabelece e retorna uma conexão com o banco de dados MySQL.
    Inclui tratamento de erros para a conexão.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        # Re-levanta a exceção para que ela possa ser tratada em níveis superiores
        raise