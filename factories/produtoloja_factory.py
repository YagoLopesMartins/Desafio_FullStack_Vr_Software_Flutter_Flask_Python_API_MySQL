from models import ProdutoLoja
from faker import Faker
import random

faker = Faker()
def create_produtoloja(db, lojas, produtos, quantidade=5):
    produtoloja = []
    for _ in range(quantidade):
        novo_produto_loja = ProdutoLoja(
            idProduto=random.choice(produtos).id,
            idLoja=random.choice(lojas).id,
            precoVenda=faker.pydecimal(left_digits=13, right_digits=3, positive=True)
        )
        produtoloja.append(novo_produto_loja)

    db.session.add_all(produtoloja)
    db.session.commit()
    return produtoloja
