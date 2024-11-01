from flask import Flask
from flask_restful import Api

from flask_cors import CORS
from sqlalchemy import event

from models import db
from config import Config
from resources import blueprint as resources_blueprint
from factories import create_lojas, create_produtos, create_produtoloja

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
api = Api(app)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(resources_blueprint)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

def populate_database():
    lojas = create_lojas(db)
    produtos = create_produtos(db)
    create_produtoloja(db, lojas, produtos)

with app.app_context():
    @event.listens_for(db.engine, "connect")
    def connect_event(dbapi_connection, connection_record):
        print("Conectado ao banco de dados com sucesso!")
    db.create_all()
    populate_database()

if __name__ == '__main__':
    app.run(debug=True)
