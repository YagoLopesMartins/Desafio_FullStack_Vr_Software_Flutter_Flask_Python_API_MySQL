from flask_restful import Resource, reqparse
from models import db, Loja, ProdutoLoja

parser = reqparse.RequestParser()
parser.add_argument('descricao', type=str, required=True, help='Descrição da loja é obrigatória.')
class LojaResource(Resource):
    def get(self, loja_id=None):
        if loja_id is None:
            lojas = Loja.query.all()
            return [
                {
                    **loja.to_dict(),
                    "loja": f"{loja.descricao} {loja.id}"
                }
                for loja in lojas
            ], 200
        else:
            loja = Loja.query.get(loja_id)
            if loja:
                loja_data = loja.to_dict()
                loja_data["loja"] = f"{loja.descricao} {loja.id}"
                return loja_data, 200
            return {'message': 'Loja não encontrada.'}, 404

    def post(self):
        args = parser.parse_args()
        nova_loja = Loja(descricao=args['descricao'])
        db.session.add(nova_loja)
        db.session.commit()
        return {"loja": nova_loja.to_dict(), "message": "Loja criada com sucesso", 'Location': f'/lojas/{nova_loja.id}'}, 201# 201 Created

    def put(self, loja_id):
        loja = Loja.query.get(loja_id)
        if not loja:
            return {'message': 'Loja não encontrada.'}, 404

        args = parser.parse_args()
        loja.descricao = args['descricao']
        db.session.commit()
        return loja.to_dict(), 200  # 200 OK

    def delete(self, loja_id):
        loja = Loja.query.get(loja_id)
        if not loja:
            return {'message': 'Loja não encontrada.'}, 404

        ProdutoLoja.query.filter_by(idLoja=loja_id).delete()
        db.session.delete(loja)
        db.session.commit()
        return {'message': 'Loja excluída com sucesso.'}, 204
