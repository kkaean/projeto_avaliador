# C:\projeto_avaliador\app\models\produto.py
from app.database.connection import get_connection

class Produto:
    def __init__(self, nome, preco, estoque, categoria, id=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.categoria = categoria

    def salvar(self):
        """
        Salva um novo produto no banco de dados.
        Após a inserção, o ID gerado é atribuído à instância.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, preco, estoque, categoria) VALUES (%s, %s, %s, %s)",
                (self.nome, self.preco, self.estoque, self.categoria)
            )
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erro ao salvar produto: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(produto_id):
        """
        Busca um produto pelo seu ID.
        Retorna um objeto Produto ou None se não encontrado.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, nome, preco, estoque, categoria FROM produtos WHERE id = %s"
            cursor.execute(query, (produto_id,))
            resultado = cursor.fetchone()
            return Produto(
                id=resultado['id'],
                nome=resultado['nome'],
                preco=resultado['preco'],
                estoque=resultado['estoque'],
                categoria=resultado['categoria']
            ) if resultado else None
        except Exception as e:
            print(f"Erro ao buscar produto por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar_todos():
        """
        Lista todos os produtos registrados no banco de dados.
        Retorna uma lista de objetos Produto.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, nome, preco, estoque, categoria FROM produtos"
            cursor.execute(query)
            resultados = cursor.fetchall()
            produtos = []
            for row in resultados:
                produtos.append(Produto(
                    id=row['id'],
                    nome=row['nome'],
                    preco=row['preco'],
                    estoque=row['estoque'],
                    categoria=row['categoria']
                ))
            return produtos
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()