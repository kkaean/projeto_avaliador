import tkinter as tk
from tkinter import messagebox
from app.controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, master):
        self.controller = ClienteController()
        self.frame = tk.Frame(master, padx=10, pady=10)
        self.frame.pack(expand=True, fill='both')

        tk.Label(self.frame, text="Nome:").grid(row=0, column=0, sticky='w', pady=2)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, sticky='ew', pady=2)

        tk.Label(self.frame, text="Email:").grid(row=1, column=0, sticky='w', pady=2)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=1, column=1, sticky='ew', pady=2)

        tk.Label(self.frame, text="Telefone:").grid(row=2, column=0, sticky='w', pady=2)
        self.telefone_entry = tk.Entry(self.frame)
        self.telefone_entry.grid(row=2, column=1, sticky='ew', pady=2)

        tk.Label(self.frame, text="Endereço:").grid(row=3, column=0, sticky='w', pady=2)
        self.endereco_entry = tk.Entry(self.frame)
        self.endereco_entry.grid(row=3, column=1, sticky='ew', pady=2)

        tk.Button(self.frame, text="Adicionar", command=self.adicionar_cliente).grid(row=4, columnspan=2, pady=10)

        # Configurar expansão de coluna para os campos de entrada
        self.frame.grid_columnconfigure(1, weight=1)

    def adicionar_cliente(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()
        endereco = self.endereco_entry.get()

        if not nome or not email: # Validação básica
            messagebox.showwarning("Entrada Inválida", "Nome e Email são campos obrigatórios.")
            return

        try:
            if self.controller.adicionar_cliente(nome, email, telefone, endereco):
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                # Limpar os campos
                self.nome_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.telefone_entry.delete(0, tk.END)
                self.endereco_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar cliente.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")