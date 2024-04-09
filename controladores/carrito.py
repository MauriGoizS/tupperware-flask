from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

carrito = Blueprint("carrito", __name__)
app = create_app()

@carrito.route('/carrito/<string:id>', methods=['GET'])
def obtener_carrito_por_id(id):
    query = {'_id': ObjectId(id)}
    try:
        resultado = mongo.db.carrito.find_one(query)
        print(resultado)

        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "carrito no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500