from app.models.cliente import Cliente

class ClienteController:
    def adicionar_cliente(self, nome, email, telefone, endereco):
        try:
            cliente = Cliente(nome, email, telefone, endereco)
            cliente.salvar()
            return True
        except Exception as e:
            print(f"Erro no controller ao adicionar cliente: {e}")
            raise # Re-levanta a exceção para que a View possa tratá-la