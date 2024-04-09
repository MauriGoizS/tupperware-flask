from flask import Flask
from config import MONGO_URI
from mongo import mongo
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['DEBUG'] = True
    app.config["MONGO_URI"] = MONGO_URI
    
    mongo.init_app(app)
    
    #resto de la configuracion de la aplicacion 
    
    return app