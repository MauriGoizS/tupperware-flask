from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify

carrito = Blueprint("carrito", __name__)
app = create_app()

@carrito.route('/carrito/<string:id>', methods=['GET'])
def obtener_carrito_por_id(id):
    query = {'_id': ObjectId(id)}
    project = {"_id": 0}
    try:
        resultado = mongo.db.carrito.find_one(query, project)
        print(resultado)

        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "carrito no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@carrito.route('/carrito/nuevo', methods=['POST'])
def crear_carrito():
    productos   = request.json["productos"]
    
    if request.method == 'POST':
        carrito = {
            "fecha_carrito": datetime.now(),
            "productos": productos
        }
    try:
        _id = mongo.db.carrito.insert_one(carrito)
        if _id:
        # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify({
                "mensaje" : "Carrito insertado con éxito",
                "_id": str(_id.inserted_id)
            }), 200
        else:
        # Si no se pudo insertar el documento, devuelve un mensaje
            return jsonify({"error": "Hubo un problema al momento de guardar el carrito"}), 500
    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus
        #necesidades
        return jsonify({"error": str(e)}), 500