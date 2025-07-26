# C:\projeto_avaliador\app\models\cliente.py
from app.database.connection import get_connection

class Cliente:
    def __init__(self, nome, email, telefone, endereco, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def salvar(self):
        """
        Salva um novo cliente no banco de dados.
        Após a inserção, o ID gerado é atribuído à instância.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s)",
                (self.nome, self.email, self.telefone, self.endereco)
            )
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erro ao salvar cliente: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(cliente_id):
        """
        Busca um cliente pelo seu ID.
        Retorna um objeto Cliente ou None se não encontrado.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, nome, email, telefone, endereco FROM clientes WHERE id = %s"
            cursor.execute(query, (cliente_id,))
            resultado = cursor.fetchone()
            return Cliente(
                id=resultado['id'],
                nome=resultado['nome'],
                email=resultado['email'],
                telefone=resultado['telefone'],
                endereco=resultado['endereco']
            ) if resultado else None
        except Exception as e:
            print(f"Erro ao buscar cliente por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar_todos():
        """
        Lista todos os clientes registrados no banco de dados.
        Retorna uma lista de objetos Cliente.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, nome, email, telefone, endereco FROM clientes"
            cursor.execute(query)
            resultados = cursor.fetchall()
            clientes = []
            for row in resultados:
                clientes.append(Cliente(
                    id=row['id'],
                    nome=row['nome'],
                    email=row['email'],
                    telefone=row['telefone'],
                    endereco=row['endereco']
                ))
            return clientes
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()