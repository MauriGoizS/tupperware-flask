from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

clien = Blueprint("cliente", __name__)
app = create_app()



@clien.route('/cliente/get_all', methods=['GET'])
def listar_cliente():
    data = mongo.db.cliente.find({})
    r = []
    for cliente in data:
        cliente['_id']=str(cliente['_id'])
        r.append(cliente)
    return r

#http://127.0.0.1:4000/cliente/get_all




@clien.route('/cliente/porNombre/<string:nombre>', methods=['GET'])
def obtener_PorNombre(nombre):
    query = {'nombre': {'$eq': nombre}}
    sort = [("nombre", 1)]
    project = {"_id": 0, "nombre": 1, "foto": 1}

    try:
        resultado = mongo.db.cliente.find(query, project).sort(sort)
        count_resultado = mongo.db.cliente.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el gmail"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #http://127.0.0.1:4000/cliente/porgmail/<string:nombre>



@clien.route('/cliente/porID/<string:id>' , methods = ['GET'])
def obtener_PorID(id):
    query={'_id': ObjectId(id)}
    project ={"_id":0}
    try:
        resultado = mongo.db.cliente.find_one(query, project)
        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# http://127.0.0.1:4000/cliente/porID/<string:id>



@clien.route('/cliente/nuevocliente', methods=['POST'])
def add_cliente():
    #from flask import request
    corr   = request.json["correo"]
    passw = request.json["password"]
    tel   = request.json["tel"]
    edad  = request.json["edad"]
    nomus   = request.json["nomuser"]
    dir   = request.json["direccion"]


    if request.method=='POST':
        product={
        "correo": corr,
        "password": passw,
        "nomuser": nomus,
        "edad": edad,
        "tel": tel,
        "direccion": dir
        }


    try:
        resultado = mongo.db.cliente.insert_one(product)
        if resultado:
        # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify({"mensaje": "Documento insertado"})
        else:
        # Si no se pudo insertar el documento, devuelve un mensaje
            return jsonify({"mensaje": "Documento no insertado"}), 404
    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus
        #necesidades
        return jsonify({"error": str(e)}), 500
    

#http://127.0.0.1:4000/cliente/nuevocliente



@clien.route('/cliente/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.cliente.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500
        
        
#http://127.0.0.1:4000/cliente/eliminar/<string:id>



@clien.route('/cliente/actualizar/<string:id>', methods=['PUT'])
def actualizar_cliente(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.cliente.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                return jsonify({"mensaje": "Documento actualizado"})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500


# http://127.0.0.1:4000/cliente/actualizar/<string:id>
    