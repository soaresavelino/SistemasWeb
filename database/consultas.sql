-- consultas.sql

-- Consulta produtos por fornecedor
DROP FUNCTION IF EXISTS consulta_produtos_fornecedor(VARCHAR);
CREATE OR REPLACE FUNCTION consulta_produtos_fornecedor(fornecedor_nome VARCHAR)
RETURNS TABLE(
    nome_produto VARCHAR,
    fornecedor VARCHAR,
    categoria VARCHAR,
    quantidade INT,
    preco NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.nome_produto, f.nome AS fornecedor, c.nome AS categoria, p.quantidade, p.preco
    FROM produtos p
    LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
    LEFT JOIN categorias c ON p.categoria_id = c.id
    WHERE f.nome ILIKE '%' || fornecedor_nome || '%'
    ORDER BY p.nome_produto;
END;
$$;

-- Consulta produtos por categoria
DROP FUNCTION IF EXISTS consulta_produtos_categoria(VARCHAR);
CREATE OR REPLACE FUNCTION consulta_produtos_categoria(categoria_nome VARCHAR)
RETURNS TABLE(
    nome_produto VARCHAR,
    categoria VARCHAR,
    fornecedor VARCHAR,
    quantidade INT,
    preco NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.nome_produto, c.nome AS categoria, f.nome AS fornecedor, p.quantidade, p.preco
    FROM produtos p
    LEFT JOIN categorias c ON p.categoria_id = c.id
    LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
    WHERE c.nome ILIKE '%' || categoria_nome || '%'
    ORDER BY p.nome_produto;
END;
$$;

-- Consulta produtos com estoque baixo
DROP FUNCTION IF EXISTS consulta_estoque_baixo(INT);
CREATE OR REPLACE FUNCTION consulta_estoque_baixo(limite INT)
RETURNS TABLE(
    nome_produto VARCHAR,
    quantidade INT,
    fornecedor VARCHAR,
    categoria VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.nome_produto, p.quantidade, f.nome AS fornecedor, c.nome AS categoria
    FROM produtos p
    LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
    LEFT JOIN categorias c ON p.categoria_id = c.id
    WHERE p.quantidade <= limite
    ORDER BY p.quantidade ASC;
END;
$$;

-- Consulta todos os produtos
DROP FUNCTION IF EXISTS consulta_todos_produtos();
CREATE OR REPLACE FUNCTION consulta_todos_produtos()
RETURNS TABLE(
    nome_produto VARCHAR,
    fornecedor VARCHAR,
    categoria VARCHAR,
    quantidade INT,
    preco NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.nome_produto, f.nome AS fornecedor, c.nome AS categoria, p.quantidade, p.preco
    FROM produtos p
    LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
    LEFT JOIN categorias c ON p.categoria_id = c.id
    ORDER BY p.nome_produto;
END;
$$;

-- Consulta histórico de ações
DROP FUNCTION IF EXISTS consulta_historico_acoes();
CREATE OR REPLACE FUNCTION consulta_historico_acoes()
RETURNS TABLE(
    id INT,
    entidade VARCHAR,
    id_entidade INT,
    acao VARCHAR,
    usuario VARCHAR,
    data_hora TIMESTAMP,
    descricao TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT h.id, h.entidade, h.id_entidade, h.acao, u.nickname, h.data_hora, h.descricao
    FROM historico_acoes h
    JOIN usuarios u ON h.id_usuario = u.id
    ORDER BY h.data_hora DESC
    LIMIT 100;
END;
$$;

-- Deletar produto e registrar no histórico
DROP FUNCTION IF EXISTS deletar_produto_e_registrar(INT, VARCHAR);
CREATE OR REPLACE FUNCTION deletar_produto_e_registrar(id_produto INT, usuario_nickname VARCHAR)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    nome_produto VARCHAR;
    id_usuario INT;
BEGIN
    SELECT p.nome_produto INTO nome_produto
    FROM produtos p
    WHERE p.id = id_produto;

    SELECT u.id INTO id_usuario
    FROM usuarios u
    WHERE u.nickname = usuario_nickname;

    DELETE FROM produtos WHERE id = id_produto;

    INSERT INTO historico_acoes(entidade, id_entidade, acao, id_usuario, descricao)
    VALUES('produto', id_produto, 'excluir', id_usuario, 'Produto "' || nome_produto || '" excluído.');
END;
$$;

-- Consulta produto por ID
DROP FUNCTION IF EXISTS consulta_produto_por_id(INT);
CREATE OR REPLACE FUNCTION consulta_produto_por_id(id_produto INT)
RETURNS TABLE(
    id INT,
    nome_produto VARCHAR,
    codigo VARCHAR,
    preco NUMERIC,
    quantidade INT,
    data_validade DATE,
    fornecedor_id INT,
    categoria_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.nome_produto, p.codigo, p.preco, p.quantidade, p.data_validade, p.fornecedor_id, p.categoria_id
    FROM produtos p
    WHERE p.id = id_produto;
END;
$$;

-- Atualizar produto
DROP FUNCTION IF EXISTS atualizar_produto(INT, VARCHAR, VARCHAR, NUMERIC, INT, DATE, INT, INT);
CREATE OR REPLACE FUNCTION atualizar_produto(
    id_produto INT,
    novo_nome VARCHAR,
    novo_codigo VARCHAR,
    novo_preco NUMERIC,
    nova_quantidade INT,
    nova_validade DATE,
    novo_fornecedor INT,
    nova_categoria INT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE produtos
    SET nome_produto = novo_nome,
        codigo = novo_codigo,
        preco = novo_preco,
        quantidade = nova_quantidade,
        data_validade = nova_validade,
        fornecedor_id = novo_fornecedor,
        categoria_id = nova_categoria
    WHERE id = id_produto;
END;
$$;

-- Existe produto
DROP FUNCTION IF EXISTS existe_produto(VARCHAR);
CREATE OR REPLACE FUNCTION existe_produto(nome_produto VARCHAR)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    qtd INT;
BEGIN
    SELECT COUNT(*) INTO qtd
    FROM produtos
    WHERE nome_produto = nome_produto;

    RETURN qtd > 0;
END;
$$;

-- Consulta todos os fornecedores
DROP FUNCTION IF EXISTS consulta_todos_fornecedores();
CREATE OR REPLACE FUNCTION consulta_todos_fornecedores()
RETURNS TABLE(
    id INT,
    nome TEXT,
    telefone TEXT,
    email TEXT,
    endereco TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        f.id, 
        f.nome::TEXT,     
        f.telefone::TEXT,  
        f.email::TEXT,     
        f.endereco::TEXT   
    FROM fornecedores f
    ORDER BY f.nome;
END;
$$ LANGUAGE plpgsql;
