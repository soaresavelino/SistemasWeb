-- Inserir categorias
INSERT INTO categorias (nome) VALUES
('Bebidas'),
('Alimentos'),
('Limpeza'),
('Pão e Padaria'),
('Higiene Pessoal'),
('Utilidades Domésticas'),
('Eletrônicos'),
('Brinquedos'),
('Esportes'),
('Pet Shop')
ON CONFLICT (nome) DO NOTHING;

-- Inserção de cargos 
INSERT INTO cargos (nome, descricao) VALUES
('gerente', 'Controle total do sistema, estoque e produtos'),
('estoquista', 'Controle parcial do estoque: pode atualizar quantidades e cadastrar produtos'),
('caixa', 'Controle básico: apenas visualizar'),
('repositor', 'Apenas visualizar produtos e estoque'),
('limpeza', 'Sem permissão: apenas visualizar')
ON CONFLICT (nome) DO NOTHING;

-- Inserção de usuários 
INSERT INTO usuarios (nome, nickname, senha, cargo_id) VALUES
('Gabriel Soares', 'gabriel', 'senha123', (SELECT id FROM cargos WHERE nome = 'gerente')),
('Ana Clara', 'ana', 'senha456', (SELECT id FROM cargos WHERE nome = 'gerente')),
('Laura Andrade', 'laura', 'senha111', (SELECT id FROM cargos WHERE nome = 'gerente')),
('Carlos Silva', 'carlos', 'senha789', (SELECT id FROM cargos WHERE nome = 'estoquista')),
('Beatriz Souza', 'beatriz', 'senha321', (SELECT id FROM cargos WHERE nome = 'estoquista')),
('Daniela Lima', 'daniela', 'senha654', (SELECT id FROM cargos WHERE nome = 'limpeza')),
('Diego Magalhães', 'diego', 'senha987', (SELECT id FROM cargos WHERE nome = 'gerente')),
('Fernanda Rocha', 'fernanda', 'senha741', (SELECT id FROM cargos WHERE nome = 'caixa')),
('Rafael Costa', 'rafael', 'senha852', (SELECT id FROM cargos WHERE nome = 'repositor')),
('Juliana Martins', 'juliana', 'senha963', (SELECT id FROM cargos WHERE nome = 'estoquista'))
ON CONFLICT (nickname) DO NOTHING;

-- Inserção de fornecedores 
INSERT INTO fornecedores (nome, telefone, email, endereco) VALUES
('Ambev', '(11) 2122-1000', 'contato@ambev.com.br', 'Rua Ambev, 123 - São Paulo, SP'),
('Raízes Agro', '(31) 3344-5566', 'contato@raizes.com.br', 'Av. Raízes, 500 - Belo Horizonte, MG'),
('TecnoSoft', '(21) 9988-7766', 'vendas@tecnosoft.com', 'Rua Tecnologia, 45 - Rio de Janeiro, RJ'),
('Distribuidora Brasil', '(41) 3322-7788', 'contato@distribuidorabrasil.com', 'Rua Central, 900 - Curitiba, PR'),
('Alimentos Naturais', '(85) 3344-5566', 'contato@alimentosnaturais.com', 'Av. Saúde, 110 - Fortaleza, CE'),
('Eletrônica Top', '(11) 3344-5566', 'vendas@eletronicatop.com.br', 'Av. Tecnologia, 200 - São Paulo, SP'),
('Brinquedos & Cia', '(31) 9988-1122', 'contato@brinquedosecia.com.br', 'Rua Diversão, 45 - Belo Horizonte, MG'),
('Pet Mundo', '(21) 2233-4455', 'contato@petmundo.com.br', 'Rua Animais, 12 - Rio de Janeiro, RJ')
ON CONFLICT (nome) DO NOTHING;

-- Inserção de produtos 
INSERT INTO produtos (nome_produto, codigo, preco, quantidade, data_validade, fornecedor_id, categoria_id) VALUES
('Cerveja Pilsen', 'CERV001', 5.50, 100, '2025-12-31',
    (SELECT id FROM fornecedores WHERE nome = 'Ambev'),
    (SELECT id FROM categorias WHERE nome = 'Bebidas')
),
('Arroz Integral', 'ARROZ01', 12.30, 50, '2024-06-30',
    (SELECT id FROM fornecedores WHERE nome = 'Raízes Agro'),
    (SELECT id FROM categorias WHERE nome = 'Alimentos')
),
('Detergente Líquido', 'LIMPE01', 7.80, 60, NULL,
    (SELECT id FROM fornecedores WHERE nome = 'Distribuidora Brasil'),
    (SELECT id FROM categorias WHERE nome = 'Limpeza')
),
('Pão de Forma Panco 500g', 'PANCO500', 7.00, 56, '2024-08-25',
    (SELECT id FROM fornecedores WHERE nome = 'Alimentos Naturais'),
    (SELECT id FROM categorias WHERE nome = 'Pão e Padaria')
),
('Sabonete Lux 85g', 'SABONETE85', 3.50, 100, '2027-10-20',
    (SELECT id FROM fornecedores WHERE nome = 'Alimentos Naturais'),
    (SELECT id FROM categorias WHERE nome = 'Higiene Pessoal')
),
('Shampoo Hidratante', 'SHAMPOO01', 15.00, 40, '2025-03-15',
    (SELECT id FROM fornecedores WHERE nome = 'Distribuidora Brasil'),
    (SELECT id FROM categorias WHERE nome = 'Higiene Pessoal')
),
('Notebook Gamer', 'NOTE001', 4500.00, 10, NULL,
    (SELECT id FROM fornecedores WHERE nome = 'TecnoSoft'),
    (SELECT id FROM categorias WHERE nome = 'Eletrônicos')
),
('Mouse Sem Fio', 'MOUSE01', 120.00, 25, NULL,
    (SELECT id FROM fornecedores WHERE nome = 'Eletrônica Top'),
    (SELECT id FROM categorias WHERE nome = 'Eletrônicos')
),
('Bola de Futebol', 'BOLA01', 90.00, 30, NULL,
    (SELECT id FROM fornecedores WHERE nome = 'Brinquedos & Cia'),
    (SELECT id FROM categorias WHERE nome = 'Esportes')
),
('Pelúcia Urso', 'PELUCIA01', 60.00, 50, NULL,
    (SELECT id FROM fornecedores WHERE nome = 'Brinquedos & Cia'),
    (SELECT id FROM categorias WHERE nome = 'Brinquedos')
),
('Ração Cães Adultos 1kg', 'RACAO01', 25.00, 80, '2025-12-31',
    (SELECT id FROM fornecedores WHERE nome = 'Pet Mundo'),
    (SELECT id FROM categorias WHERE nome = 'Pet Shop')
),
('Detergente Pó Limpeza Total', 'DETPO01', 10.00, 70, NULL,
    (SELECT id FROM fornecedores WHERE nome = 'Distribuidora Brasil'),
    (SELECT id FROM categorias WHERE nome = 'Limpeza')
)
ON CONFLICT (codigo) DO NOTHING;

-- Inserção de histórico de ações 
INSERT INTO historico_acoes (entidade, id_entidade, acao, id_usuario, descricao) VALUES
('produto', 1, 'inserir', (SELECT id FROM usuarios WHERE nickname = 'daniela'), 'Produto Cerveja Pilsen criado pelo administrador'),
('produto', 2, 'inserir', (SELECT id FROM usuarios WHERE nickname = 'daniela'), 'Produto Arroz Integral criado pelo administrador'),
('usuario', (SELECT id FROM usuarios WHERE nickname = 'gabriel'), 'inserir', (SELECT id FROM usuarios WHERE nickname = 'daniela'), 'Usuário Gabriel Soares criado pelo administrador'),
('usuario', (SELECT id FROM usuarios WHERE nickname = 'carlos'), 'inserir', (SELECT id FROM usuarios WHERE nickname = 'daniela'), 'Usuário Carlos Silva criado pelo administrador'),
('fornecedor', (SELECT id FROM fornecedores WHERE nome = 'Ambev'), 'inserir', (SELECT id FROM usuarios WHERE nickname = 'daniela'), 'Fornecedor Ambev cadastrado pelo administrador'),
('produto', (SELECT id FROM produtos WHERE nome_produto = 'Notebook Gamer'), 'inserir', (SELECT id FROM usuarios WHERE nickname = 'gabriel'), 'Notebook Gamer cadastrado no sistema'),
('produto', (SELECT id FROM produtos WHERE nome_produto = 'Ração Cães Adultos 1kg'), 'inserir', (SELECT id FROM usuarios WHERE nickname = 'gabriel'), 'Ração Cães Adultos cadastrada no sistema'),
('fornecedor', (SELECT id FROM fornecedores WHERE nome = 'Pet Mundo'), 'inserir', (SELECT id FROM usuarios WHERE nickname = 'gabriel'), 'Fornecedor Pet Mundo cadastrado')
ON CONFLICT DO NOTHING;
