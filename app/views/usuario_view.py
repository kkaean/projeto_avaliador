# C:\projeto_avaliador\app\views\usuario_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from app.controllers.usuario_controller import UsuarioController

class UsuarioView:
    def __init__(self, master):
        self.master = master
        self.controller = UsuarioController()
        self.frame = tk.Frame(master, padx=10, pady=10)
        self.frame.pack(expand=True, fill='both')

        self.create_widgets()
        self.carregar_usuarios()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill='both')

        # --- Aba de Registrar Usuário ---
        self.registro_frame = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.registro_frame, text="Registrar Usuário")

        tk.Label(self.registro_frame, text="Username:").grid(row=0, column=0, sticky='w', pady=2)
        self.username_reg_entry = tk.Entry(self.registro_frame)
        self.username_reg_entry.grid(row=0, column=1, sticky='ew', pady=2)

        tk.Label(self.registro_frame, text="Senha:").grid(row=1, column=0, sticky='w', pady=2)
        self.password_reg_entry = tk.Entry(self.registro_frame, show="*") # show="*" esconde a senha
        self.password_reg_entry.grid(row=1, column=1, sticky='ew', pady=2)

        tk.Label(self.registro_frame, text="Repetir Senha:").grid(row=2, column=0, sticky='w', pady=2)
        self.password_confirm_reg_entry = tk.Entry(self.registro_frame, show="*")
        self.password_confirm_reg_entry.grid(row=2, column=1, sticky='ew', pady=2)

        tk.Label(self.registro_frame, text="Nível (role):").grid(row=3, column=0, sticky='w', pady=2)
        self.role_options = ['operador', 'admin']
        self.role_var = tk.StringVar(self.registro_frame)
        self.role_var.set(self.role_options[0]) # Default value
        self.role_menu = ttk.Combobox(self.registro_frame, textvariable=self.role_var, values=self.role_options, state="readonly")
        self.role_menu.grid(row=3, column=1, sticky='ew', pady=2)


        tk.Button(self.registro_frame, text="Registrar", command=self.registrar_usuario).grid(row=4, columnspan=2, pady=10)
        self.registro_frame.grid_columnconfigure(1, weight=1)

        # --- Aba de Login (Autenticação) ---
        self.login_frame = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.login_frame, text="Login")

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky='w', pady=2)
        self.username_login_entry = tk.Entry(self.login_frame)
        self.username_login_entry.grid(row=0, column=1, sticky='ew', pady=2)

        tk.Label(self.login_frame, text="Senha:").grid(row=1, column=0, sticky='w', pady=2)
        self.password_login_entry = tk.Entry(self.login_frame, show="*")
        self.password_login_entry.grid(row=1, column=1, sticky='ew', pady=2)

        tk.Button(self.login_frame, text="Login", command=self.autenticar_usuario).grid(row=2, columnspan=2, pady=10)
        self.login_frame.grid_columnconfigure(1, weight=1)

        # --- Aba de Listar Usuários ---
        self.lista_frame = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.lista_frame, text="Listar Usuários")

        self.user_tree = ttk.Treeview(self.lista_frame, columns=("ID", "Username", "Role", "Criado Em"), show="headings")
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Role", text="Role")
        self.user_tree.heading("Criado Em", text="Criado Em")

        self.user_tree.column("ID", width=50, anchor='center')
        self.user_tree.column("Username", width=120)
        self.user_tree.column("Role", width=80, anchor='center')
        self.user_tree.column("Criado Em", width=150, anchor='center')

        self.user_tree.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(self.user_tree, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')


    def registrar_usuario(self):
        username = self.username_reg_entry.get()
        password = self.password_reg_entry.get()
        confirm_password = self.password_confirm_reg_entry.get()
        role = self.role_var.get()

        if password != confirm_password:
            messagebox.showerror("Erro de Senha", "As senhas não coincidem!")
            return

        try:
            if self.controller.registrar_usuario(username, password, role):
                messagebox.showinfo("Sucesso", f"Usuário '{username}' registrado com sucesso!")
                self.limpar_campos_registro()
                self.carregar_usuarios()
            # O controller levanta exceções para erros, então não há 'else' aqui.
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def autenticar_usuario(self):
        username = self.username_login_entry.get()
        password = self.password_login_entry.get()

        usuario_autenticado = self.controller.autenticar_usuario(username, password)
        if usuario_autenticado:
            messagebox.showinfo("Login Sucesso", f"Bem-vindo, {usuario_autenticado.username}! Nível: {usuario_autenticado.role}")
            # Aqui você pode fechar a janela de login e abrir a janela principal do sistema,
            # ou armazenar o usuário autenticado em algum lugar para controle de acesso.
            self.limpar_campos_login()
            # self.master.destroy() # Exemplo: fechar a janela de login após sucesso
        else:
            messagebox.showerror("Login Falhou", "Nome de usuário ou senha inválidos.")

    def limpar_campos_registro(self):
        self.username_reg_entry.delete(0, tk.END)
        self.password_reg_entry.delete(0, tk.END)
        self.password_confirm_reg_entry.delete(0, tk.END)
        self.role_var.set(self.role_options[0])

    def limpar_campos_login(self):
        self.username_login_entry.delete(0, tk.END)
        self.password_login_entry.delete(0, tk.END)

    def carregar_usuarios(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        usuarios = self.controller.listar_usuarios()
        for user_data in usuarios:
            created_at_str = user_data['created_at'].strftime('%Y-%m-%d %H:%M:%S') if 'created_at' in user_data and user_data['created_at'] else 'N/A'
            self.user_tree.insert("", "end", values=(
                user_data['id'],
                user_data['username'],
                user_data['role'],
                created_at_str
            ))