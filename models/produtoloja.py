from sqlalchemy import Column, Integer, ForeignKey, Numeric
from . import db
class ProdutoLoja(db.Model):
    __tablename__ = 'produtoloja'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idLoja = Column(Integer, ForeignKey('loja.id'), nullable=False)
    idProduto = Column(Integer, ForeignKey('produto.id'), nullable=False)
    precoVenda = Column(Numeric(13, 3), nullable=True)

    produto = db.relationship('Produto', back_populates='produtos_loja')
    loja = db.relationship('Loja', back_populates='produtos')

    def to_dict(self):
        return {
            "id": self.id,
            "idLoja": self.idLoja,
            "idProduto": self.idProduto,
            "precoVenda": float(self.precoVenda)
        }
