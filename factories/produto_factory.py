from models import Produto
from faker import Faker

faker = Faker()
def create_produtos(db, quantidade=5):
    produtos = [
        Produto(
            descricao=faker.text(50),
            custo=faker.pydecimal(left_digits=13, right_digits=3, positive=True),
            imagem=faker.binary(length=64)
        )
        for _ in range(quantidade)
    ]
    db.session.add_all(produtos)
    db.session.commit()
    return produtos
