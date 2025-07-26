# Sistema de Controle de Loja (Tkinter + MySQL)

Este é um sistema de controle de loja básico desenvolvido em Python utilizando a biblioteca `tkinter` para a interface gráfica e `MySQL` para o banco de dados. O sistema permite gerenciar clientes, produtos, vendas e usuários, com um fluxo de autenticação inicial.

---

## 🚀 Funcionalidades

* **Autenticação de Usuários:**
    * Tela de Login inicial.
    * Registro de novos usuários (com hash seguro de senhas via `bcrypt`).
    * Listagem de usuários registrados.
    * Controle de acesso básico por `role` (administrador vs. operador) para o gerenciamento de usuários.
* **Gerenciamento de Clientes:**
    * Cadastro de novos clientes.
    * Listagem de clientes existentes.
    * Busca e atualização de dados de clientes.
    * Exclusão de clientes.
* **Gerenciamento de Produtos:**
    * Cadastro de novos produtos (nome, preço, estoque, categoria).
    * Listagem de produtos existentes.
    * Busca e atualização de dados de produtos.
    * Exclusão de produtos.
* **Gerenciamento de Vendas:**
    * Registro de novas vendas associadas a um cliente.
    * Adição de múltiplos itens a uma venda, com cálculo automático do total.
    * Listagem de vendas com detalhes dos itens e do cliente.
    * Atualização do estoque do produto ao adicionar um item à venda.
* **Interface Gráfica Intuitiva:**
    * Utiliza `tkinter` com `ttk` para uma experiência de usuário agradável.
    * Telas separadas para cada funcionalidade.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **tkinter**: Biblioteca padrão do Python para interfaces gráficas.
* **mysql-connector-python**: Driver para conexão com o banco de dados MySQL.
* **python-dotenv**: Para gerenciar variáveis de ambiente (credenciais do banco de dados).
* **bcrypt**: Para hashing seguro de senhas.
* **MySQL**: Sistema de gerenciamento de banco de dados relacional.

---

## ⚙️ Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto em sua máquina:

### 1. Pré-requisitos

* **Python 3.x** instalado.
* **MySQL Server** instalado e em execução (ex: XAMPP, WAMP, Docker, ou instalação nativa).

### 2. Clonar o Repositório (se aplicável)

Se este projeto estiver em um repositório Git:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd sistema_controle_loja