import sys
import os

# Adiciona o diretório pai (projeto_avaliador) ao sys.path para que os imports funcionem corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from app.views.cliente_view import ClienteView
from app.views.produto_view import ProdutoView
from app.views.venda_view import VendaView
from app.views.usuario_view import UsuarioView # NOVA IMPORTAÇÃO

def abrir_cliente():
    janela = tk.Toplevel()
    janela.title("Cadastro de Clientes")
    ClienteView(janela)

def abrir_produto():
    janela = tk.Toplevel()
    janela.title("Cadastro de Produtos")
    ProdutoView(janela)

def abrir_venda():
    janela = tk.Toplevel()
    janela.title("Registro de Vendas")
    VendaView(janela)

def abrir_usuario(): # NOVA FUNÇÃO
    janela = tk.Toplevel()
    janela.title("Gerenciamento de Usuários")
    UsuarioView(janela)


def main():
    root = tk.Tk()
    root.title("Sistema de Controle de Loja")
    root.geometry("350x300") # Aumentado um pouco para acomodar o novo botão

    # Centraliza a janela na tela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    btn_cliente = tk.Button(root, text="Cadastro de Clientes", width=28, command=abrir_cliente)
    btn_cliente.pack(pady=10)

    btn_produto = tk.Button(root, text="Cadastro de Produtos", width=28, command=abrir_produto)
    btn_produto.pack(pady=10)

    btn_venda = tk.Button(root, text="Registro de Vendas", width=28, command=abrir_venda)
    btn_venda.pack(pady=10)

    btn_usuario = tk.Button(root, text="Gerenciar Usuários", width=28, command=abrir_usuario) # NOVO BOTÃO
    btn_usuario.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()