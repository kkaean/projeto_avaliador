# C:\projeto_avaliador\app\views\venda_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from app.controllers.venda_controller import VendaController

class VendaView:
    def __init__(self, master):
        self.master = master
        self.controller = VendaController()
        self.frame = tk.Frame(master, padx=10, pady=10)
        self.frame.pack(expand=True, fill='both')

        self.create_widgets()
        self.carregar_vendas() # Carrega as vendas ao iniciar a view

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(expand=True, fill='both')

        # --- Aba de Registrar Venda ---
        self.registro_frame = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.registro_frame, text="Registrar Venda")

        tk.Label(self.registro_frame, text="ID do Cliente:").grid(row=0, column=0, sticky='w', pady=2)
        self.cliente_id_entry = tk.Entry(self.registro_frame)
        self.cliente_id_entry.grid(row=0, column=1, sticky='ew', pady=2)

        # Botão para iniciar uma nova venda (com total zero, itens serão adicionados separadamente)
        btn_registrar = tk.Button(self.registro_frame, text="Registrar Nova Venda", command=self.adicionar_venda_simples)
        btn_registrar.grid(row=1, column=0, columnspan=2, pady=10)

        # Seção para adicionar itens a uma venda existente
        item_frame = tk.LabelFrame(self.registro_frame, text="Adicionar Itens à Venda Existente", padx=10, pady=10)
        item_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(item_frame, text="ID da Venda:").grid(row=0, column=0, sticky='w', pady=2)
        self.venda_id_item_entry = tk.Entry(item_frame)
        self.venda_id_item_entry.grid(row=0, column=1, sticky='ew', pady=2)

        tk.Label(item_frame, text="ID do Produto:").grid(row=1, column=0, sticky='w', pady=2)
        self.produto_id_item_entry = tk.Entry(item_frame)
        self.produto_id_item_entry.grid(row=1, column=1, sticky='ew', pady=2)

        tk.Label(item_frame, text="Quantidade:").grid(row=2, column=0, sticky='w', pady=2)
        self.quantidade_item_entry = tk.Entry(item_frame)
        self.quantidade_item_entry.grid(row=2, column=1, sticky='ew', pady=2)

        btn_add_item = tk.Button(item_frame, text="Adicionar Item", command=self.adicionar_item_venda)
        btn_add_item.grid(row=3, column=0, columnspan=2, pady=10)

        # Configurar expansão de coluna para os campos de entrada
        item_frame.grid_columnconfigure(1, weight=1)
        self.registro_frame.grid_columnconfigure(1, weight=1)


        # --- Aba de Listar Vendas ---
        self.lista_frame = tk.Frame(self.notebook, padx=10, pady=10)
        self.notebook.add(self.lista_frame, text="Listar Vendas")

        self.tree = ttk.Treeview(self.lista_frame, columns=("ID", "Cliente", "Total", "Data"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Data", text="Data")

        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Cliente", width=150)
        self.tree.column("Total", width=100, anchor='e')
        self.tree.column("Data", width=150, anchor='center')

        self.tree.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Evento para clicar duas vezes em uma venda e mostrar detalhes
        self.tree.bind("<Double-1>", self.mostrar_detalhes_venda)

    def adicionar_venda_simples(self):
        """
        Adiciona uma venda com cliente_id e total zero (para ser atualizado com itens posteriormente).
        """
        try:
            cliente_id = int(self.cliente_id_entry.get())
            total = 0.0 # Venda inicializada com total 0, itens serão adicionados depois

            # O controller.adicionar_venda não retorna o ID da venda, precisaria de ajuste se fosse usar aqui.
            # Por enquanto, apenas tenta registrar.
            if self.controller.adicionar_venda(cliente_id, total):
                messagebox.showinfo("Sucesso", "Venda principal registrada com sucesso! Agora adicione os itens usando o ID da venda.")
                self.limpar_campos_venda()
                self.carregar_vendas()
            # else: o controller levanta exceção, então o except abaixo pegará
        except ValueError as ve:
            messagebox.showerror("Erro de Entrada", str(ve))
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")


    def adicionar_item_venda(self):
        """
        Adiciona um item a uma venda existente.
        """
        try:
            venda_id = int(self.venda_id_item_entry.get())
            produto_id = int(self.produto_id_item_entry.get())
            quantidade = int(self.quantidade_item_entry.get())

            if self.controller.adicionar_item_a_venda(venda_id, produto_id, quantidade):
                messagebox.showinfo("Sucesso", "Item adicionado à venda com sucesso!")
                self.limpar_campos_item()
                self.carregar_vendas() # Recarrega a lista para refletir possíveis mudanças no total (se implementado)
            # else: o controller levanta exceção, então o except abaixo pegará
        except ValueError as ve:
            messagebox.showerror("Erro de Entrada", str(ve))
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")


    def limpar_campos_venda(self):
        self.cliente_id_entry.delete(0, tk.END)

    def limpar_campos_item(self):
        self.venda_id_item_entry.delete(0, tk.END)
        self.produto_id_item_entry.delete(0, tk.END)
        self.quantidade_item_entry.delete(0, tk.END)

    def carregar_vendas(self):
        # Limpa os itens existentes na Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        vendas_com_detalhes = self.controller.listar_vendas_com_detalhes()
        for venda_data in vendas_com_detalhes:
            data_formatada = venda_data['data_venda'].strftime('%Y-%m-%d %H:%M:%S')
            self.tree.insert("", "end", iid=venda_data['id'],
                             values=(venda_data['id'], venda_data['nome_cliente'],
                                     f"R$ {venda_data['total']:.2f}", data_formatada))

    def mostrar_detalhes_venda(self, event):
        """
        Abre uma nova janela para exibir os detalhes de uma venda selecionada,
        incluindo os itens comprados.
        """
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            return

        # 'iid' é o ID do item na Treeview, que definimos como o ID da venda
        venda_id = self.tree.item(item_selecionado, "iid")
        venda_detalhes = self.controller.buscar_venda_por_id(venda_id)

        if not venda_detalhes:
            messagebox.showerror("Erro", "Venda não encontrada para detalhes.")
            return

        detalhes_window = tk.Toplevel(self.master)
        detalhes_window.title(f"Detalhes da Venda ID: {venda_detalhes['id']}")
        detalhes_window.transient(self.master)
        detalhes_window.grab_set()

        tk.Label(detalhes_window, text=f"Cliente: {venda_detalhes['nome_cliente']} (ID: {venda_detalhes['cliente_id']})").pack(pady=5)
        tk.Label(detalhes_window, text=f"Data: {venda_detalhes['data_venda'].strftime('%Y-%m-%d %H:%M:%S')}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Total da Venda: R$ {venda_detalhes['total']:.2f}").pack(pady=5)

        tk.Label(detalhes_window, text="--- Itens Comprados ---").pack(pady=10)

        if venda_detalhes['itens_comprados']:
            itens_tree = ttk.Treeview(detalhes_window, columns=("Produto", "Quantidade", "Preço Unit."), show="headings")
            itens_tree.heading("Produto", text="Produto")
            itens_tree.heading("Quantidade", text="Qtd.")
            itens_tree.heading("Preço Unit.", text="Preço Unit.")

            itens_tree.column("Produto", width=150)
            itens_tree.column("Quantidade", width=70, anchor='center')
            itens_tree.column("Preço Unit.", width=100, anchor='e')

            for item in venda_detalhes['itens_comprados']:
                itens_tree.insert("", "end", values=(item['nome_produto'], item['quantidade'], f"R$ {item['preco_unitario']:.2f}"))

            itens_tree.pack(fill='both', expand=True, padx=10, pady=5)
        else:
            tk.Label(detalhes_window, text="Nenhum item registrado para esta venda.").pack(pady=5)

        tk.Button(detalhes_window, text="Fechar", command=detalhes_window.destroy).pack(pady=10)