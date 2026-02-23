import psycopg2

def conecta_bd():
    return psycopg2.connect(
        host="localhost",
        database="loja",
        user="usuario",
        password="12345"
    )