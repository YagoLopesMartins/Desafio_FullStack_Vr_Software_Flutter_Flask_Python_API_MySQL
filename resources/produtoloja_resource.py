from flask_restful import Resource, reqparse
from models import db, ProdutoLoja, Produto, Loja
from flask import Blueprint, jsonify, request

produtoloja_bp = Blueprint('produtoloja', __name__)
class ProdutoLojaResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('idLoja', type=int, required=True, help="ID da loja é obrigatório")
    parser.add_argument('idProduto', type=int, required=True, help="ID do produto é obrigatório")
    parser.add_argument('precoVenda', type=float, required=True, help="Preço de venda é obrigatório")
    @produtoloja_bp.route('/produtoloja', methods=['GET'])
    def get(self):
        page = request.args.get('page', default=1, type=int)  # Padrão para 1
        per_page = request.args.get('per_page', default=10, type=int)  # Padrão para 10

        # Consultar os dados com a paginação
        produtos_lojas_query = db.session.query(
            ProdutoLoja.id,
            ProdutoLoja.idProduto,
            ProdutoLoja.precoVenda,
            Loja.id.label("loja_id"),
            Loja.descricao.label("loja_descricao")
        ).join(Loja, ProdutoLoja.idLoja == Loja.id)

        # Calcular o total de produtos
        total_produtos = produtos_lojas_query.count()

        # Aplicar a paginação
        produtos_lojas = produtos_lojas_query.offset((page - 1) * per_page).limit(per_page).all()

        response = {
            "total": total_produtos,
            "page": page,
            "per_page": per_page,
            "produtos": []
        }

        for produto_loja in produtos_lojas:
            response["produtos"].append({
                "id": produto_loja.id,
                "idProduto": produto_loja.idProduto,
                "precoVenda": produto_loja.precoVenda,
                "loja": f"{produto_loja.loja_descricao} {produto_loja.loja_id}"
            })

        return jsonify(response)
    @produtoloja_bp.route('/produtoloja', methods=['POST'])
    def post(self):
        args = self.parser.parse_args()

        if not Loja.query.get(args['idLoja']):
            return {'message': 'Loja não encontrada'}, 404
        if not Produto.query.get(args['idProduto']):
            return {'message': 'Produto não encontrado'}, 400

        produto_loja_existente = ProdutoLoja.query.filter_by(idLoja=args['idLoja'], idProduto=args['idProduto']).first()
        if produto_loja_existente:
            return {'message': 'Este produto já possui um preço de venda para a loja especificada.'}, 400

        novo_produto_loja = ProdutoLoja(
            idLoja=args['idLoja'],
            idProduto=args['idProduto'],
            precoVenda=args['precoVenda']
        )
        db.session.add(novo_produto_loja)
        db.session.commit()

        return {"message": "Preço de venda cadastrado com sucesso.", "produto_loja": novo_produto_loja.to_dict()}, 201

    @produtoloja_bp.route('/produtoloja/<int:id>', methods=['PUT'])
    def put(self, id):
        args = self.parser.parse_args()

        produto_loja = ProdutoLoja.query.get(id)

        if not produto_loja:
            return {'message': 'ProdutoLoja não encontrado.'}, 404

        produto_loja_existente = ProdutoLoja.query.filter(
            ProdutoLoja.idLoja == args['idLoja'],
            ProdutoLoja.idProduto == args['idProduto'],
            ProdutoLoja.id != id
        ).first()

        if produto_loja_existente:
            return {'message': 'Não é permitido mais que um preço de venda para a mesma loja.'}, 400

        produto_loja.idLoja = args['idLoja']
        produto_loja.idProduto = args['idProduto']
        produto_loja.precoVenda = args['precoVenda']
        db.session.commit()

        return {"message": "Preço de venda atualizado com sucesso.", "produto_loja": produto_loja.to_dict()}, 200

    @produtoloja_bp.route('/produtoloja/<int:id>', methods=['DELETE'])
    def delete(self, id):

        produto_loja = ProdutoLoja.query.get(id)
        if produto_loja is None:
            return {'message': 'ProdutoLoja não encontrado'}, 404

        db.session.delete(produto_loja)
        db.session.commit()
        return {"message": "ProdutoLoja excluído com sucesso"}, 200
