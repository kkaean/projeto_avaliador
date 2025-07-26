import tkinter as tk
from tkinter import messagebox
from app.controllers.produto_controller import ProdutoController

class ProdutoView:
    def __init__(self, master):
        self.controller = ProdutoController()
        self.frame = tk.Frame(master, padx=10, pady=10)
        self.frame.pack(expand=True, fill='both')

        tk.Label(self.frame, text="Nome:").grid(row=0, column=0, sticky='w', pady=2)
        self.nome_entry = tk.Entry(self.frame)
        self.nome_entry.grid(row=0, column=1, sticky='ew', pady=2)

        tk.Label(self.frame, text="Preço:").grid(row=1, column=0, sticky='w', pady=2)
        self.preco_entry = tk.Entry(self.frame)
        self.preco_entry.grid(row=1, column=1, sticky='ew', pady=2)

        tk.Label(self.frame, text="Estoque:").grid(row=2, column=0, sticky='w', pady=2)
        self.estoque_entry = tk.Entry(self.frame)
        self.estoque_entry.grid(row=2, column=1, sticky='ew', pady=2)

        tk.Label(self.frame, text="Categoria:").grid(row=3, column=0, sticky='w', pady=2)
        self.categoria_entry = tk.Entry(self.frame)
        self.categoria_entry.grid(row=3, column=1, sticky='ew', pady=2)

        tk.Button(self.frame, text="Adicionar Produto", command=self.adicionar_produto).grid(row=4, columnspan=2, pady=10)

        # Configurar expansão de coluna para os campos de entrada
        self.frame.grid_columnconfigure(1, weight=1)

    def adicionar_produto(self):
        nome = self.nome_entry.get()
        preco = self.preco_entry.get()
        estoque = self.estoque_entry.get()
        categoria = self.categoria_entry.get()

        if not nome or not preco or not estoque: # Validação básica
            messagebox.showwarning("Entrada Inválida", "Nome, Preço e Estoque são campos obrigatórios.")
            return

        try:
            # O controller agora lida com a conversão de tipo e validação
            if self.controller.adicionar_produto(nome, preco, estoque, categoria):
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                self.nome_entry.delete(0, tk.END)
                self.preco_entry.delete(0, tk.END)
                self.estoque_entry.delete(0, tk.END)
                self.categoria_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar produto.")
        except ValueError as ve:
            messagebox.showerror("Erro de Entrada", str(ve))
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")