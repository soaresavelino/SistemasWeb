
# 📘 CSI606-2026-02 – Proposta de Trabalho Final

**Discente:** Gabriel Soares

O projeto consiste no desenvolvimento de um sistema simples para gerenciar o estoque de um supermercado. O sistema permitirá cadastrar produtos, categorias e fornecedores, além de consultar e atualizar quantidades em estoque.

## Tema

O trabalho tem como tema o desenvolvimento de um **Sistema de Gerenciamento de Estoque de Supermercado**.

---

## 1. Funcionalidades implementadas

O sistema terá as seguintes funcionalidades básicas:

- Cadastro, edição e exclusão de produtos
- Consulta e busca de produtos
- Atualização de quantidades em estoque
- Associação de produtos a categorias e fornecedores previamente cadastrados
- Controle de acesso por tipo de usuário

---

## 2. Funcionalidades previstas e não implementadas

- Controle financeiro
- Integração com sistema de vendas (PDV)
- Relatórios avançados ou análises

Essas funcionalidades não foram incluídas para manter o foco no gerenciamento básico de estoque, conforme o escopo definido.

---

## 3. Outras funcionalidades implementadas

- Organização do projeto seguindo o padrão MVC
- Separação entre Model, View e Controller
- Controle de permissões por tipo de usuário

---

## 4. Principais desafios e dificuldades

Durante o desenvolvimento do projeto, os principais desafios foram:

- Organizar corretamente a aplicação utilizando o padrão MVC
- Separar a lógica das rotas do acesso ao banco de dados
- Implementar controle de permissões por tipo de usuário
- Realizar a integração entre Flask e PostgreSQL

As dificuldades foram superadas por meio de testes das tecnologias utilizadas.

---

## 5. Instruções para instalação e execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/soaresavelino/SistemasWeb.git
```

### 2️⃣ Instalar as dependências
```bash
pip install flask
pip install psycopg2
pip install flask-wtf
```

### 3️⃣ Executar a aplicação
```bash
python loja.py
```

Após a execução, a aplicação estará disponível em: http://localhost:5000

---

## 6. Referências

FLASK. *Flask Documentation*. Disponível em: https://flask.palletsprojects.com/. Acesso em: 23 fev. 2026.

POSTGRESQL. *PostgreSQL Documentation*. Disponível em: https://www.postgresql.org/docs/. Acesso em: 23 fev. 2026.

PYTHON SOFTWARE FOUNDATION. *Python Documentation*. Disponível em: https://docs.python.org/3/. Acesso em: 23 fev. 2026.