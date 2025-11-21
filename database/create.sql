-- DROP TABLES 
DROP TABLE IF EXISTS historico_acoes CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS fornecedores CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS cargos CASCADE;

-- Tabela cargos
CREATE TABLE cargos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT
);

-- Tabela usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cargo_id INT NOT NULL,
    CONSTRAINT fk_usuario_cargo FOREIGN KEY (cargo_id) REFERENCES cargos(id)
);

-- Tabela fornecedores
CREATE TABLE fornecedores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(255),
    endereco VARCHAR(255)
);

-- Tabela categorias
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela produtos
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    preco NUMERIC(10, 2) NOT NULL CHECK (preco >= 0),
    quantidade INT NOT NULL CHECK (quantidade >= 0),
    data_validade DATE,
    fornecedor_id INT,
    categoria_id INT,
    CONSTRAINT fk_fornecedor FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id) ON DELETE SET NULL,
    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

-- Tabela historico_acoes
CREATE TABLE historico_acoes (
    id SERIAL PRIMARY KEY,
    entidade VARCHAR(50) NOT NULL,         -- 'produto', 'usuario', etc
    id_entidade INT NOT NULL,              -- id do produto ou usuário afetado
    acao VARCHAR(20) NOT NULL,             -- 'inserir', 'editar', 'excluir', 'mostrar'
    id_usuario INT NOT NULL,                -- quem fez a ação
    data_hora TIMESTAMP NOT NULL DEFAULT NOW(),
    descricao TEXT,
    CONSTRAINT fk_historico_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);