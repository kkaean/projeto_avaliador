# C:\projeto_avaliador\app\controllers\usuario_controller.py
from app.models.usuario import Usuario

class UsuarioController:
    def registrar_usuario(self, username, password, role='operador'):
        """
        Tenta registrar um novo usuário.
        Retorna True se o registro for bem-sucedido, False caso contrário.
        Levanta ValueError se o usuário já existir ou dados inválidos.
        """
        if not username or not password:
            raise ValueError("Username e senha são obrigatórios.")
        if len(password) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")

        if Usuario.buscar_por_username(username):
            raise ValueError("Nome de usuário já existe. Escolha outro.")

        try:
            # O construtor de Usuario já faz o hash da senha
            novo_usuario = Usuario(username=username, password_plain=password, role=role)
            novo_usuario.salvar()
            return True
        except Exception as e:
            print(f"Erro no controller ao registrar usuário: {e}")
            return False

    def autenticar_usuario(self, username, password):
        """
        Tenta autenticar um usuário.
        Retorna o objeto Usuario se a autenticação for bem-sucedida, None caso contrário.
        """
        if not username or not password:
            return None # Não autentica se dados vazios

        usuario = Usuario.buscar_por_username(username)
        if usuario and usuario.verificar_senha(password):
            return usuario # Retorna o objeto Usuario autenticado
        return None # Credenciais inválidas

    def listar_usuarios(self):
        """
        Lista todos os usuários registrados (sem o hash da senha).
        """
        return Usuario.listar_todos()