# API de Gestão de Produto e Loja

Esta API fornece endpoints para gerenciar produtos, lojas e a relação entre eles, incluindo a configuração de preços de venda de produtos específicos em lojas. A API é implementada em Flask com SQLAlchemy e utiliza Flask-RESTful para simplificar a criação dos recursos.

## Tecnologias Utilizadas
- Python 3
- Flask
- Flask-RESTful
- SQLAlchemy
- Flask-SQLAlchemy (para integração do SQLAlchemy ao Flask)
- Marshmallow (para serialização)
- Banco de Dados: MySQL 

## Endpoints

### Produtos
- **`GET /produtos`**: Retorna uma lista de produtos, paginação e com suporte a filtros opcionais, incluindo `codigo`, `descricao`, `custo` e `precoVenda`.
- **`GET /produtos/<produto_id>`**: Retorna os detalhes de um produto específico.
- **`POST /produtos`**: Cria um novo produto com os dados fornecidos.
- **`PUT /produtos/<produto_id>`**: Atualiza as informações de um produto específico.
- **`DELETE /produtos/<produto_id>`**: Exclui um produto específico.

### Lojas
- **`GET /lojas`**: Retorna uma lista de lojas com seus detalhes.
- **`GET /lojas/<loja_id>`**: Retorna os detalhes de uma loja específica.
- **`POST /lojas`**: Cria uma nova loja.
- **`PUT /lojas/<loja_id>`**: Atualiza as informações de uma loja específica.
- **`DELETE /lojas/<loja_id>`**: Exclui uma loja específica.

### ProdutoLoja (Relacionamento Produto-Loja)
- **`GET /produtoloja`**: Retorna a lista de associações entre produtos e lojas, incluindo informações de preço de venda.
- **`POST /produtoloja`**: Cria uma nova associação de produto em loja com um preço de venda.
- **`PUT /produtoloja/<id_loja>/<id_produto>`**: Atualiza o preço de venda de um produto específico em uma loja.
- **`DELETE /produtoloja/<id_loja>/<id_produto>`**: Remove a associação de um produto em uma loja.

## Regras de Validação
- **Campos Obrigatórios**: Todos os campos obrigatórios devem ser preenchidos, caso contrário, será retornada uma mensagem de erro.
- **Preço Único por Loja e Produto**: Não é permitido cadastrar mais de um preço de venda para o mesmo produto em uma loja. Caso um registro duplicado seja tentado, um erro será retornado.
- **Formato de Preço**: O preço de venda deve estar no formato decimal `(13,3)`, aceitando até 3 casas decimais.

## Exemplo de Uso no Postman

### Exemplo de Requisição POST para Criar um Produto
```json
POST /produtos
{
  "descricao": "Produto Exemplo",
  "custo": 100.50,
  "imagem": "url_da_imagem"
}
```

## Configuração do Projeto
### Instalação e Configuração de Dependências

- Clone o repositório.
- Instale as dependências (pip install -r requirements.txt)
- Defina as variáveis para no .env
- Crie seu banco de dados ou utilize o que está disponível no diretório utils
- Execute o arquivo da raiz: python app.py

  ```
  flask db upgrade
  flask run
  ```
- Acesse a API no navegador ou no Postman: http://localhost:5000

### Estrutura do Projeto

```
.
├── factories/           # Fabrica de dados baseado nos modelos (popula banco de dados)
├── models/              # Modelos SQLAlchemy para Produto, Loja e ProdutoLoja
├── resources/           # Recursos Flask-RESTful para endpoints
├── tests/               # Testes unitários das principais funcionalidades
├── utils/               # Contem endpoints do Postman apra testes de API e o banco de dados
├── .env                 # Arquivo com variaveis de ambientes
├── app.py               # Arquivo principal da aplicação
├── config.py            # Arquivo de conexão com banco de dados
└── README.md            # Documentação da API
├── requirements.txt     # Lista de bibliotecas e tecnologias utilizadas
```

#### Para dúvidas ou contribuições, fique à vontade para abrir uma issue ou pull request ou entrar em contato no e-mail: yagolopesmartins777@gmail.com

