import psycopg2
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_wtf.csrf import CSRFProtect

from formularios import FormularioProduto, FormularioUsuario, FormularioConsulta

app = Flask(__name__)
app.secret_key = 'estoquebd'

csrf = CSRFProtect(app)

class Produto:
    def __init__(self, id, nome_produto, codigo, preco, quantidade, data_validade, fornecedor_id, nome_fornecedor=None, categoria_id=None, nome_categoria=None):
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

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

def conecta_bd():
    return psycopg2.connect(
        host="localhost",
        database="loja",
        user="usuario",
        password="12345"
    )

def cargo_usuario_logado():
    usuario_logado = session.get('usuario_logado')
    if not usuario_logado:
        return None
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('''
        SELECT c.nome FROM usuarios u
        JOIN cargos c ON u.cargo_id = c.id
        WHERE u.nickname = %s
    ''', (usuario_logado,))
    resultado = cur.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def registrar_historico(entidade, id_entidade, acao, descricao=None):
    usuario_logado = session.get('usuario_logado')
    if not usuario_logado:
        return

    conn = conecta_bd()
    cur = conn.cursor()

    cur.execute('SELECT id FROM usuarios WHERE nickname = %s', (usuario_logado,))
    resultado = cur.fetchone()
    if resultado is None:
        conn.close()
        return
    id_usuario = resultado[0]

    cur.execute(
        'INSERT INTO historico_acoes (entidade, id_entidade, acao, id_usuario, descricao) VALUES (%s, %s, %s, %s, %s)',
        (entidade, id_entidade, acao, id_usuario, descricao)
    )
    conn.commit()
    conn.close()

def buscar_produtos(nome=None, fornecedor=None):
    conn = conecta_bd()
    cur = conn.cursor()

    sql = '''
    SELECT p.id, p.nome_produto, p.codigo, p.preco, p.quantidade, p.data_validade, p.fornecedor_id, f.nome,
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
    return [Produto(*produto) for produto in produtos]

def adicionar_produto(produto):
    conn = conecta_bd()
    cur = conn.cursor()

    cur.execute(
        '''INSERT INTO produtos (nome_produto, codigo, preco, quantidade, data_validade, fornecedor_id, categoria_id)
           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
        (produto.nome_produto, produto.codigo, produto.preco, produto.quantidade, produto.data_validade, produto.fornecedor_id, produto.categoria_id)
    )
    conn.commit()
    conn.close()

def buscar_usuario_por_nickname_cargo(nickname, cargo_id):
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT nome, nickname, senha FROM usuarios WHERE nickname = %s AND cargo_id = %s', (nickname, cargo_id))
    usuario = cur.fetchone()
    conn.close()
    if usuario:
        return Usuario(*usuario)
    return None

def buscar_fornecedores():
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT id, nome FROM fornecedores ORDER BY nome')
    fornecedores = cur.fetchall()
    conn.close()
    return fornecedores

def buscar_categorias():
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT id, nome FROM categorias ORDER BY nome')
    categorias = cur.fetchall()
    conn.close()
    return categorias

def buscar_cargos():
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT id, nome FROM cargos ORDER BY nome')
    cargos = cur.fetchall()
    conn.close()
    return cargos


# Controle de permissões (pode ajustar os cargos que podem fazer cada ação aqui):
PERMISSOES = {
    'criar': ['gerente', 'estoquista'],
    'editar': ['gerente', 'estoquista'],
    'deletar': ['gerente'],
    
}

# ----------------- INÍCIO DAS ALTERAÇÕES -----------------


@app.route('/')
def index():
    proxima = request.args.get('proxima', url_for('produtos'))
    form = FormularioUsuario()
    cargos = buscar_cargos()
    form.cargo.choices = [(c[0], c[1]) for c in cargos]
    return render_template('login.html', proxima=proxima, form=form)

# Rota da lista de produtos 
@app.route('/produtos')
def produtos():
    nome = request.args.get('nome', '')
    fornecedor = request.args.get('fornecedor', '')
    produtos_lista = buscar_produtos(nome=nome if nome else None, fornecedor=fornecedor if fornecedor else None)
    return render_template('lista.html', titulo='CadastraFácil', produtos=produtos_lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('index', proxima=url_for('novo')))

    cargo = cargo_usuario_logado()
    if cargo not in PERMISSOES['criar']:
        flash('Acesso negado: você não tem permissão para criar produtos.', 'danger')
        return redirect(url_for('produtos'))

    form = FormularioProduto()
    fornecedores = buscar_fornecedores()
    categorias = buscar_categorias()

    form.fornecedor.choices = [(f[0], f[1]) for f in fornecedores]
    form.categoria.choices = [(c[0], c[1]) for c in categorias]

    return render_template('novo.html', titulo='Cadastro de Produtos', form=form)

@app.route('/criar', methods=['POST'])
def criar():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('index', proxima=url_for('novo')))

    cargo = cargo_usuario_logado()
    if cargo not in PERMISSOES['criar']:
        flash('Acesso negado: você não tem permissão para criar produtos.', 'danger')
        return redirect(url_for('produtos'))

    form = FormularioProduto(request.form)

    fornecedores = buscar_fornecedores()
    categorias = buscar_categorias()

    form.fornecedor.choices = [(f[0], f[1]) for f in fornecedores]
    form.categoria.choices = [(c[0], c[1]) for c in categorias]

    if not form.validate_on_submit():
        flash('Formulário inválido ou dados faltando.', 'danger')
        return redirect(url_for('novo'))

    nome_produto = form.nome_produto.data
    codigo = form.codigo.data
    preco = form.preco.data
    quantidade = form.quantidade.data
    data_validade = form.data_validade.data if form.data_validade.data else None  
    fornecedor_id = form.fornecedor.data
    categoria_id = form.categoria.data

    conn = conecta_bd()
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM produtos WHERE nome_produto = %s', (nome_produto,))
    existe_produto = cur.fetchone()[0] > 0

    if existe_produto:
        flash(f'Produto com o nome "{nome_produto}" já existe!')
        conn.close()
        return redirect(url_for('novo'))

    novo_produto = Produto(None, nome_produto, codigo, preco, quantidade, data_validade, fornecedor_id, None, categoria_id)
    adicionar_produto(novo_produto)

    cur.execute('SELECT id FROM produtos WHERE nome_produto = %s ORDER BY id DESC LIMIT 1', (nome_produto,))
    novo_id = cur.fetchone()[0]

    registrar_historico('produto', novo_id, 'inserir', f'Produto "{nome_produto}" criado.')

    conn.close()

    flash('Produto adicionado com sucesso!')
    return redirect(url_for('produtos'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('index', proxima=url_for('editar', id=id)))

    cargo = cargo_usuario_logado()
    if cargo not in PERMISSOES['editar']:
        flash('Acesso negado: você não tem permissão para editar produtos.', 'danger')
        return redirect(url_for('produtos'))

    form = FormularioProduto()
    conn = conecta_bd()
    cur = conn.cursor()

    # Preenche fornecedores e categorias
    cur.execute('SELECT id, nome FROM fornecedores ORDER BY nome')
    form.fornecedor.choices = [(f[0], f[1]) for f in cur.fetchall()]
    cur.execute('SELECT id, nome FROM categorias ORDER BY nome')
    form.categoria.choices = [(c[0], c[1]) for c in cur.fetchall()]

    if request.method == 'POST' and form.validate_on_submit():
        # Converte data para None se estiver vazia
        data_validade = form.data_validade.data
        if isinstance(data_validade, str) and data_validade.strip() == '':
            data_validade = None

        fornecedor_id = int(form.fornecedor.data) if form.fornecedor.data else None
        categoria_id = int(form.categoria.data) if form.categoria.data else None

        # Chama função de atualização no banco
        cur.execute(
            'SELECT atualizar_produto(%s,%s,%s,%s,%s,%s,%s,%s)',
            (
                id,
                form.nome_produto.data,
                form.codigo.data,
                form.preco.data,
                form.quantidade.data,
                data_validade,
                fornecedor_id,
                categoria_id
            )
        )
        conn.commit()

        registrar_historico('produto', id, 'editar', f'Produto "{form.nome_produto.data}" atualizado.')
        conn.close()

        flash('Produto atualizado com sucesso!')
        return redirect(url_for('produtos'))

    else:
        # Carrega produto do banco para preencher o formulário
        cur.execute('SELECT * FROM consulta_produto_por_id(%s)', (id,))
        produto = cur.fetchone()
        conn.close()

        if produto:
            form.nome_produto.data = produto[1]
            form.codigo.data = produto[2]
            form.preco.data = produto[3]
            form.quantidade.data = produto[4]
            form.data_validade.data = produto[5]  
            form.fornecedor.data = produto[6]
            form.categoria.data = produto[7]
        else:
            flash('Produto não encontrado.')
            return redirect(url_for('produtos'))

    return render_template('editar.html', titulo='Edição de Produto', id=id, form=form)



@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('index'))

    cargo = cargo_usuario_logado()
    if cargo not in PERMISSOES['deletar']:
        flash('Acesso negado: você não tem permissão para deletar produtos.', 'danger')
        return redirect(url_for('produtos'))

    conn = conecta_bd()
    cur = conn.cursor()
    
    # Chama a função do banco
    cur.execute('SELECT deletar_produto_e_registrar(%s, %s)', (id, session['usuario_logado']))
    conn.commit()
    conn.close()

    flash('Produto removido com sucesso!')
    return redirect(url_for('produtos'))


@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)
    cargos = buscar_cargos()
    form.cargo.choices = [(c[0], c[1]) for c in cargos]

    if form.validate_on_submit():
        usuario = buscar_usuario_por_nickname_cargo(form.nickname.data, form.cargo.data)
        if usuario:
            if form.senha.data == usuario.senha:
                session['usuario_logado'] = usuario.nickname
                flash(f'{usuario.nickname} logado com sucesso!')

                proxima_pagina = request.form.get('proxima', url_for('produtos'))
                return redirect(proxima_pagina)
            else:
                flash('Senha incorreta.')
        else:
            flash('Usuário ou cargo incorretos.')
    else:
        flash('Formulário inválido.')

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/historico')
def historico():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('index', proxima=url_for('historico')))
    

    conn = conecta_bd()
    cur = conn.cursor()

    
    cur.execute('SELECT * FROM consulta_historico_acoes()')
    acoes = cur.fetchall()
    conn.close()

    return render_template('historico.html', acoes=acoes)

# ----------------- FIM DAS ALTERAÇÕES -----------------

@app.route('/consultas', methods=['GET', 'POST'])
def consultas():
    form = FormularioConsulta()
    resultados = []
    colunas = []
    erro = None

    if form.validate_on_submit():
        consulta_tipo = form.tipo.data
        parametro = form.parametro.data.strip()

        try:
            conn = conecta_bd()
            cur = conn.cursor()

            
            if consulta_tipo == 'produtos_fornecedor' and parametro:
                cur.execute('SELECT * FROM consulta_produtos_fornecedor(%s)', (parametro,))
            
            elif consulta_tipo == 'produtos_categoria' and parametro:
                cur.execute('SELECT * FROM consulta_produtos_categoria(%s)', (parametro,))
            
            elif consulta_tipo == 'estoque_baixo':
                limite = int(parametro) if parametro.isdigit() else 10
                cur.execute('SELECT * FROM consulta_estoque_baixo(%s)', (limite,))
            
            elif consulta_tipo == 'todos_produtos':
                cur.execute('SELECT * FROM consulta_todos_produtos()')
                
            elif consulta_tipo == 'todos_fornecedores':
                cur.execute('SELECT * FROM consulta_todos_fornecedores()')

        

            resultados = cur.fetchall()
            colunas = [desc[0] for desc in cur.description]

            cur.close()
            conn.close()

        except Exception as e:
            erro = f'Erro ao executar a consulta: {e}'

    return render_template('consultas.html', form=form, resultados=resultados, colunas=colunas, erro=erro)

if __name__ == '__main__':
    app.run(debug=True)




    