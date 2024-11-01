import base64

from flask import Blueprint, request, jsonify
from flask_restful import Resource
from models import db, Produto, ProdutoLoja

produto_bp = Blueprint('produto', __name__)
class ProdutoResource(Resource):
    @produto_bp.route('/produtos', methods=['GET'])
    def get(self, produto_id=None):
        if produto_id is None:
             codigo = request.args.get('codigo', type=int)
             descricao = request.args.get('descricao', type=str)
             custo = request.args.get('custo', type=float)
             precoVenda = request.args.get('precoVenda', type=float)

             page = request.args.get('page', 1, type=int)
             per_page = request.args.get('per_page', 10, type=int)

             query = db.session.query(Produto).join(ProdutoLoja, Produto.id == ProdutoLoja.idProduto)

             if codigo:
                 query = query.filter(Produto.id == codigo)
             if descricao:
                 query = query.filter(Produto.descricao.ilike(f"%{descricao}%"))
             if custo is not None:
                 query = query.filter(Produto.custo == custo)
             if precoVenda is not None:
                 query = query.filter(ProdutoLoja.precoVenda == precoVenda)

             paginated_result = query.paginate(page=page, per_page=per_page, error_out=False)
             produtos = paginated_result.items

             response = {
                 "total": paginated_result.total,
                 "page": paginated_result.page,
                 "per_page": paginated_result.per_page,
                 "pages": paginated_result.pages,
                 "produtos": [produto.to_dict() for produto in produtos]
             }

             return jsonify(response)
        else:
            produto = Produto.query.get_or_404(produto_id)
            if produto:
                return produto.to_dict(), 200
            return {'message': 'Produto não encontrado.'}, 404
    @produto_bp.route('/produtos', methods=['POST'])
    def post(self):
        data = request.get_json()

        imagem_base64 = data.get("imagem")
        imagem_binaria = base64.b64decode(imagem_base64) if imagem_base64 else None

        novo_produto = Produto(
            descricao=data['descricao'],
            custo=data['custo'],
            imagem=imagem_binaria
        )

        db.session.add(novo_produto)
        db.session.commit()

        return {"produto": novo_produto.to_dict(),"message": "Produto criado com sucesso"}, 201

    @produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
    def put(self, produto_id):
        produto = Produto.query.get(produto_id)
        if not produto:
            return {'message': 'Produto não encontrado'}, 404

        data = request.get_json()
        produto.descricao = data.get('descricao', produto.descricao)
        produto.custo = data.get('custo', produto.custo)

        if 'imagem' in data:
            if isinstance(data['imagem'], str):
                produto.imagem = base64.b64decode(data['imagem'])
            else:
                produto.imagem = None

        db.session.commit()
        return {'message': 'Produto atualizado com sucesso', 'produto': produto.to_dict()}, 200

    @produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
    def delete(self, produto_id):
        produto = Produto.query.get(produto_id)
        if not produto:
            return {'message': 'Produto não encontrado'}, 404

        ProdutoLoja.query.filter_by(idProduto=produto_id).delete()
        db.session.delete(produto)
        db.session.commit()
        return {'message': 'Produto excluído com sucesso'}, 201
