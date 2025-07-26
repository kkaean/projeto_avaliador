# C:\projeto_avaliador\app\models\usuario.py
from app.database.connection import get_connection
import bcrypt # Importa a biblioteca para hashing de senhas
from datetime import datetime

class Usuario:
    def __init__(self, username, password_hash=None, password_plain=None, role='operador', id=None, created_at=None):
        self.id = id
        self.username = username
        self.role = role
        self.created_at = created_at if created_at else datetime.now()

        if password_plain:
            # Hash da senha se uma senha em texto puro for fornecida
            self.password_hash = self._hash_password(password_plain)
        elif password_hash:
            # Usa o hash fornecido se já existir (para carregar do DB)
            self.password_hash = password_hash
        else:
            raise ValueError("Uma senha (texto puro ou hash) deve ser fornecida.")

    def _hash_password(self, password):
        """Gera um hash bcrypt para a senha fornecida."""
        # bcrypt.gensalt() gera um salt (valor aleatório) para cada hash, tornando-o único
        # O 'rounds' controla a complexidade, 12 é um bom valor padrão.
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        return hashed.decode('utf-8') # Decodifica para string para salvar no DB

    def verificar_senha(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def salvar(self):
        """
        Salva um novo usuário (ou atualiza um existente se tiver ID) no banco de dados.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.id: # Atualizar usuário existente
                query = "UPDATE usuarios SET username = %s, password_hash = %s, role = %s WHERE id = %s"
                valores = (self.username, self.password_hash, self.role, self.id)
            else: # Inserir novo usuário
                query = "INSERT INTO usuarios (username, password_hash, role) VALUES (%s, %s, %s)"
                valores = (self.username, self.password_hash, self.role)

            cursor.execute(query, valores)
            conn.commit()
            if not self.id:
                self.id = cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erro ao salvar usuário: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_username(username):
        """
        Busca um usuário pelo seu nome de usuário.
        Retorna um objeto Usuario ou None se não encontrado.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, username, password_hash, role, created_at FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            resultado = cursor.fetchone()
            if resultado:
                return Usuario(
                    id=resultado['id'],
                    username=resultado['username'],
                    password_hash=resultado['password_hash'], # Passa o hash diretamente
                    role=resultado['role'],
                    created_at=resultado['created_at']
                )
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por username: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def listar_todos():
        """
        Lista todos os usuários registrados.
        Retorna uma lista de objetos Usuario (sem revelar o hash da senha diretamente, se for para exibir).
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, username, role, created_at FROM usuarios" # Não seleciona o password_hash
            cursor.execute(query)
            resultados = cursor.fetchall()
            usuarios = []
            for row in resultados:
                # Ao criar o objeto Usuario para listar, passamos um hash dummy
                # Ou podemos criar um objeto mais simples sem o hash.
                # Para fins de demonstração, passaremos um hash temporário se necessário.
                # Ou, melhor, construímos um dicionário para a lista.
                usuarios.append({
                    'id': row['id'],
                    'username': row['username'],
                    'role': row['role'],
                    'created_at': row['created_at']
                })
            return usuarios
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()