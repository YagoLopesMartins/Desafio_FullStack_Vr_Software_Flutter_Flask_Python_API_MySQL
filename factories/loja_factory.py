from models import Loja
from faker import Faker

faker = Faker()
def create_lojas(db, quantidade=5):
    lojas = [Loja(descricao=faker.company()) for _ in range(quantidade)]
    db.session.add_all(lojas)
    db.session.commit()
    return lojas

