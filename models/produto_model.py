from models.database import conecta_bd

class Produto:
    def __init__(
        self,
        id,
        nome_produto,
        codigo,
        preco,
        quantidade,
        data_validade,
        fornecedor_id,
        nome_fornecedor=None,
        categoria_id=None,
        nome_categoria=None
    ):
        self.id = id
        self.nome_produto = nome_produto
        self.codigo = codigo
        self.preco = preco
        self.quantidade = quantidade
        self.data_validade = data_validade
        self.fornecedor_id = fornecedor_id
        self.nome_fornecedor = nome_fornecedor
        self.categoria_id = categoria_id
        self.nome_categoria = nome_categoria


def buscar_produtos(nome=None, fornecedor=None):
    conn = conecta_bd()
    cur = conn.cursor()

    sql = '''
        SELECT p.id, p.nome_produto, p.codigo, p.preco, p.quantidade,
               p.data_validade, p.fornecedor_id, f.nome,
               p.categoria_id, c.nome
        FROM produtos p
        LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE TRUE
    '''
    params = []

    if nome:
        sql += ' AND p.nome_produto ILIKE %s'
        params.append(f'%{nome}%')

    if fornecedor:
        sql += ' AND f.nome ILIKE %s'
        params.append(f'%{fornecedor}%')

    cur.execute(sql, params)
    produtos = cur.fetchall()
    conn.close()

    return [Produto(*p) for p in produtos]


def adicionar_produto(produto):
    conn = conecta_bd()
    cur = conn.cursor()

    cur.execute(
        '''
        INSERT INTO produtos
        (nome_produto, codigo, preco, quantidade, data_validade, fornecedor_id, categoria_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''',
        (
            produto.nome_produto,
            produto.codigo,
            produto.preco,
            produto.quantidade,
            produto.data_validade,
            produto.fornecedor_id,
            produto.categoria_id
        )
    )
    conn.commit()
    conn.close()


def buscar_fornecedores():
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT id, nome FROM fornecedores ORDER BY nome')
    dados = cur.fetchall()
    conn.close()
    return dados


def buscar_categorias():
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT id, nome FROM categorias ORDER BY nome')
    dados = cur.fetchall()
    conn.close()
    return dados