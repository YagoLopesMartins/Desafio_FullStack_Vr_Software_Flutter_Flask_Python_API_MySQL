from flask_restful import Api
from flask import Blueprint

from .produto_resource import ProdutoResource
from .loja_resource import LojaResource
from .produtoloja_resource import ProdutoLojaResource

blueprint = Blueprint('resources', __name__)
api = Api(blueprint)

api.add_resource(LojaResource, '/lojas', '/lojas/<int:loja_id>')
api.add_resource(ProdutoResource, '/produtos', '/produtos/<int:produto_id>')
api.add_resource(ProdutoLojaResource, '/produtoloja', '/produtoloja/<int:id>')
