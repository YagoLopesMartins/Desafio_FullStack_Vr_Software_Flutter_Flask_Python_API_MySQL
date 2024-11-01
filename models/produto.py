from . import db
import base64
class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(60), nullable=False)
    custo = db.Column(db.Numeric(13, 3), nullable=True)
    imagem = db.Column(db.LargeBinary, nullable=True)

    produtos_loja = db.relationship('ProdutoLoja', back_populates='produto')

    def to_dict(self):
        result = {
            "id": self.id,
            "descricao": self.descricao,
            "custo": float(self.custo),
        }
        if self.imagem:
            try:
                result["imagem"] = base64.b64encode(self.imagem).decode('utf-8')
            except Exception as e:
                result["imagem"] = "Dados da imagem inválidos: " + str(e)
        else:
            result["imagem"] = None
        return result
