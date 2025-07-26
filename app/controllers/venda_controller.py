# C:\projeto_avaliador\app\controllers\venda_controller.py
from app.models.venda import Venda
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.database.connection import get_connection

class VendaController:
    def __init__(self):
        pass

    def adicionar_venda(self, cliente_id, total):
        """
        Adiciona uma nova venda no sistema.
        Retorna True em caso de sucesso, False caso contrário.
        """
        if not isinstance(cliente_id, int) or cliente_id <= 0:
            raise ValueError("ID do cliente inválido.")
        if not isinstance(total, (int, float)) or total < 0:
            raise ValueError("Total da venda inválido.")

        cliente_existente = Cliente.buscar_por_id(cliente_id)
        if not cliente_existente:
             raise ValueError("Cliente com o ID especificado não encontrado.")

        try:
            venda = Venda(cliente_id=cliente_id, total=total)
            venda.salvar()
            return True
        except Exception as e:
            print(f"Erro ao adicionar venda: {e}")
            return False

    def listar_vendas_com_detalhes(self):
        """
        Lista todas as vendas e inclui os nomes do cliente e os itens da venda.
        Retorna uma lista de dicionários, onde cada dicionário representa uma venda
        com seus detalhes (incluindo 'nome_cliente' e 'itens_comprados').
        """
        vendas = Venda.listar_todas()
        lista_completa = []
        for venda in vendas:
            # Buscar nome do cliente
            cliente = Cliente.buscar_por_id(venda.cliente_id)
            nome_cliente = cliente.nome if cliente else "Desconhecido"

            # Buscar itens da venda
            itens_comprados = venda.get_itens_venda()

            lista_completa.append({
                'id': venda.id,
                'cliente_id': venda.cliente_id,
                'nome_cliente': nome_cliente,
                'total': venda.total,
                'data_venda': venda.data_venda,
                'itens_comprados': itens_comprados
            })
        return lista_completa

    def buscar_venda_por_id(self, venda_id):
        """
        Busca uma venda pelo seu ID e inclui detalhes do cliente e itens.
        """
        if not isinstance(venda_id, int) or venda_id <= 0:
            raise ValueError("ID da venda inválido.")
        venda = Venda.buscar_por_id(venda_id)
        if venda:
            cliente = Cliente.buscar_por_id(venda.cliente_id)
            nome_cliente = cliente.nome if cliente else "Desconhecido"
            itens_comprados = venda.get_itens_venda()

            return {
                'id': venda.id,
                'cliente_id': venda.cliente_id,
                'nome_cliente': nome_cliente,
                'total': venda.total,
                'data_venda': venda.data_venda,
                'itens_comprados': itens_comprados
            }
        return None

    def adicionar_item_a_venda(self, venda_id, produto_id, quantidade):
        """
        Adiciona um item a uma venda existente e atualiza o total da venda,
        tudo dentro de uma única transação.
        """
        # Validações de entrada
        if not isinstance(venda_id, int) or venda_id <= 0:
            raise ValueError("ID da venda inválido.")
        if not isinstance(produto_id, int) or produto_id <= 0:
            raise ValueError("ID do produto inválido.")
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade inválida.")

        # Buscar venda e produto para obter informações necessárias
        # (Estas chamadas abrem e fecham suas próprias conexões, o que é aceitável para simples lookups)
        venda_existente = Venda.buscar_por_id(venda_id)
        if not venda_existente:
            raise ValueError("Venda não encontrada.")

        produto_existente = Produto.buscar_por_id(produto_id)
        if not produto_existente:
            raise ValueError("Produto não encontrado.")

        preco_unitario = produto_existente.preco

        # Gerenciamento da transação para inserção do item e atualização do total
        conn = None
        cursor = None
        try:
            conn = get_connection() # Abre UMA conexão para esta operação composta
            cursor = conn.cursor()

            # 1. Inserir o novo item na tabela item_venda
            query_insert_item = "INSERT INTO item_venda (venda_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
            valores_item = (venda_id, produto_id, quantidade, preco_unitario)
            cursor.execute(query_insert_item, valores_item)

            # 2. Recalcular o total COMPLETO da venda a partir dos itens já inseridos
            query_recalculate_total = """
                SELECT SUM(quantidade * preco_unitario)
                FROM item_venda
                WHERE venda_id = %s
            """
            cursor.execute(query_recalculate_total, (venda_id,))
            novo_total_calculado = cursor.fetchone()[0] # Pega o valor da soma

            # Garante que o total seja 0.0 se não houver itens
            if novo_total_calculado is None:
                novo_total_calculado = 0.0

            # 3. Atualizar o campo 'total' na tabela 'vendas'
            query_update_venda_total = "UPDATE vendas SET total = %s WHERE id = %s"
            cursor.execute(query_update_venda_total, (novo_total_calculado, venda_id))

            conn.commit() # Confirma AMBAS as operações (inserção do item e atualização do total)
            return True
        except Exception as e:
            if conn:
                conn.rollback() # Desfaz AMBAS as operações em caso de erro
            print(f"Erro ao adicionar item à venda ou atualizar total: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close() # Garante que a conexão seja fechada