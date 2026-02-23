from flask import session
from models.database import conecta_bd

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


def buscar_usuario_por_nickname_cargo(nickname, cargo_id):
    conn = conecta_bd()
    cur = conn.cursor()

    cur.execute(
        'SELECT nome, nickname, senha FROM usuarios WHERE nickname = %s AND cargo_id = %s',
        (nickname, cargo_id)
    )

    dados = cur.fetchone()
    conn.close()

    return Usuario(*dados) if dados else None


def buscar_cargos():
    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute('SELECT id, nome FROM cargos ORDER BY nome')
    cargos = cur.fetchall()
    conn.close()
    return cargos


def cargo_usuario_logado():
    usuario = session.get('usuario_logado')
    if not usuario:
        return None

    conn = conecta_bd()
    cur = conn.cursor()
    cur.execute(
        '''
        SELECT c.nome
        FROM usuarios u
        JOIN cargos c ON u.cargo_id = c.id
        WHERE u.nickname = %s
        ''',
        (usuario,)
    )
    dado = cur.fetchone()
    conn.close()

    return dado[0] if dado else None

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