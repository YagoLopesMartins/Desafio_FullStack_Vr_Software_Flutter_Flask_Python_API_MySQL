from . import db
class Loja(db.Model):
    __tablename__ = 'loja'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(60), nullable=False)

    produtos = db.relationship('ProdutoLoja', back_populates='loja')

    def to_dict(self):
        return {"id": self.id, "descricao": self.descricao}
