from app.models.produto import Produto

class ProdutoController:
    def adicionar_produto(self, nome, preco, estoque, categoria):
        try:
            # Converte preco e estoque para os tipos corretos
            preco_float = float(preco)
            estoque_int = int(estoque)

            produto = Produto(nome, preco_float, estoque_int, categoria)
            produto.salvar()
            return True
        except ValueError as ve:
            print(f"Erro de validação no controller ao adicionar produto: {ve}")
            raise ValueError("Dados de preço ou estoque inválidos. Verifique se são números.")
        except Exception as e:
            print(f"Erro no controller ao adicionar produto: {e}")
            raise # Re-levanta a exceção