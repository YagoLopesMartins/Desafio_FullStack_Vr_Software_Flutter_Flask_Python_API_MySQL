from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .loja import Loja
from .produto import Produto
from .produtoloja import ProdutoLoja