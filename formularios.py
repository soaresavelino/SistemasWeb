from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DecimalField, IntegerField, DateField, validators
from wtforms.validators import Optional

class FormularioProduto(FlaskForm):
    nome_produto = StringField('Nome do Produto', [validators.DataRequired(), validators.Length(min=1, max=100)])
    codigo = StringField('Código', [validators.DataRequired(), validators.Length(min=1, max=50)])
    preco = DecimalField('Preço', places=2, rounding=None,
                         validators=[validators.DataRequired(), validators.NumberRange(min=0)])
    quantidade = IntegerField('Quantidade', validators=[validators.DataRequired(), validators.NumberRange(min=0)])
    data_validade = DateField('Data de Validade', format='%Y-%m-%d', validators=[Optional()])  # agora opcional (corrigido)
    fornecedor = SelectField('Fornecedor', coerce=int, validators=[validators.DataRequired()])
    categoria = SelectField('Categoria', coerce=int, validators=[validators.DataRequired()])
    salvar = SubmitField('Salvar')
    
class FormularioUsuario(FlaskForm):
    nickname = StringField('Usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=50)])
    cargo = SelectField('Cargo', coerce=int, validators=[validators.DataRequired()])
    login = SubmitField('Login')

class FormularioConsulta(FlaskForm):
    tipo = SelectField('Tipo de Consulta', choices=[
        ('produtos_fornecedor', 'Produtos por Fornecedor'),
        ('produtos_categoria', 'Produtos por Categoria'),
        ('estoque_baixo', 'Estoque Baixo'),
        ('todos_produtos', 'Todos os Produtos'),
        ('todos_fornecedores', 'Todos os Fornecedores')
    ], validators=[validators.DataRequired()])

    parametro = StringField('Parâmetro (nome do fornecedor, categoria ou limite de estoque)',
                            validators=[validators.Optional()])
    
    consultar = SubmitField('Consultar')
