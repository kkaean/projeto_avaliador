# C:\projeto_avaliador\app\models\venda.py
from app.database.connection import get_connection
from datetime import datetime

class Venda:
    def __init__(self, cliente_id, total, id=None, data_venda=None):
        self.id = id
        self.cliente_id = cliente_id
        self.total = total
        self.data_venda = data_venda if data_venda else datetime.now()

    def salvar(self):
        """
        Salva uma nova venda no banco de dados.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO vendas (cliente_id, total, data_venda) VALUES (%s, %s, %s)"
            valores = (self.cliente_id, self.total, self.data_venda)
            cursor.execute(query, valores)
            conn.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erro ao salvar venda: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(venda_id):
        """
        Busca uma venda pelo seu ID.
        Retorna um objeto Venda ou None se não encontrado.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, cliente_id, total, data_venda FROM vendas WHERE id = %s"
            cursor.execute(query, (venda_id,))
            resultado = cursor.fetchone()
            return Venda(
                id=resultado['id'],
                cliente_id=resultado['cliente_id'],
                total=resultado['total'],
                data_venda=resultado['data_venda']
            ) if resultado else None
        except Exception as e:
            print(f"Erro ao buscar venda por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar_todas():
        """
        Lista todas as vendas registradas no banco de dados.
        Retorna uma lista de objetos Venda.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, cliente_id, total, data_venda FROM vendas ORDER BY data_venda DESC"
            cursor.execute(query)
            resultados = cursor.fetchall()
            vendas = []
            for row in resultados:
                vendas.append(Venda(
                    id=row['id'],
                    cliente_id=row['cliente_id'],
                    total=row['total'],
                    data_venda=row['data_venda']
                ))
            return vendas
        except Exception as e:
            print(f"Erro ao listar vendas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_itens_venda(self):
        """
        Retorna uma lista de dicionários com os detalhes dos produtos desta venda.
        Cada dicionário contém: nome_produto, quantidade, preco_unitario.
        """
        if not self.id:
            return []

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.nome AS nome_produto, iv.quantidade, iv.preco_unitario
                FROM item_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                WHERE iv.venda_id = %s
            """
            cursor.execute(query, (self.id,))
            itens = cursor.fetchall()
            return itens
        except Exception as e:
            print(f"Erro ao obter itens da venda: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()