from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

marc = Blueprint("marca", __name__)
app = create_app()



@marc.route('/marca/get_all', methods=['GET'])
def listar_marca():
    data = mongo.db.marca.find({})
    r = []
    for marca in data:
        marca['_id']=str(marca['_id'])
        r.append(marca)
    return r
    

#http://127.0.0.1:4000/marca/get_all


@marc.route('/marca/porID/<string:id>' ,methods = ['GET'])
def obtener_marcID(id):
    query={'_id': ObjectId(id)}
    project = {"_id":0, "nombre": 1 ,"tel": 1 , "propietario": 1,"rfc":1}
    try:
        resultado =mongo.db.marca.find_one(query,project)
        if resultado:
            return jsonify(resultado)
        else: 
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# http://127.0.0.1:4000/marca/porID/<string:id>
    

@marc.route('/marca/nuevaMarca', methods=['POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.json["nombre"]
        propietario = request.json["propietario"]
        rfc = request.json["rfc"]
        tel = request.json["tel"]
        fot = request.json["foto"]
        # Suponiendo que tienes una base de datos MongoDB configurada con Flask-PyMongo
        # Asegúrate de importar las bibliotecas necesarias y configurar la conexión a la base de datos
        # por ejemplo:
        # from flask_pymongo import pymongo
        # from flask import jsonify

        marca = {
            "nombre": nombre,
            "propietario": propietario,
            "rfc": rfc,
            "tel": tel,
            "foto": fot
        }

        try:
            resultado = mongo.db.marca.insert_one(marca)
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "Marca insertada correctamente"}), 201
            else:
                # Si no se pudo insertar la marca, devuelve un mensaje
                return jsonify({"mensaje": "Error al insertar la marca"}), 404
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500


# http://127.0.0.1:4000/marca/nuevaMarca
        
@marc.route('/marca/actualizar/<string:id>', methods=['PUT'])
def actualizar_marca(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.marca.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                return jsonify({"mensaje": "Documento actualizado"})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500

# http://127.0.0.1:4000/marca/actualizar/<string:id>
    


@marc.route('/marca/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.marca.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500
        
# http://127.0.0.1:4000/marca/eliminar/<string:id>
        


        

@marc.route('/marca/porNombre/<string:nombre>', methods=['GET'])
def obtener_ProNombre(nombre):
    query = {'nombre': {'$eq': nombre}}
    sort = [("nombre", 1)]
    project = {"_id": 0, "nombre": 1,"propietario":1, "tel": 1, "rfc": 1}

    try:
        resultado = mongo.db.marca.find(query, project).sort(sort)
        count_resultado = mongo.db.marca.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el nombre"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
