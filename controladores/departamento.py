from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

depar = Blueprint("departamento", __name__)
app = create_app()



@depar.route('/departamento/get_all', methods=['GET'])
def listar_departamento():
    data = mongo.db.departamento.find({})
    r = []
    for departamento in data:
        departamento['_id']=str(departamento['_id'])
        r.append(departamento)
    return r

#http://127.0.0.1:4000/departamento/get_all




@depar.route('/departamento/porNombre/<string:nombre>', methods=['GET'])
def obtener_PorNombre(nombre):
    query = {'nombre': {'$eq': nombre}}
    sort = [("nombre", 1)]
    project = {"_id": 0, "nombre": 1, "foto": 1}

    try:
        resultado = mongo.db.departamento.find(query, project).sort(sort)
        count_resultado = mongo.db.departamento.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el gmail"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #http://127.0.0.1:4000/departamento/porgmail/<string:nombre>



@depar.route('/departamento/porID/<string:id>' , methods = ['GET'])
def obtener_PorID(id):
    query={'_id': ObjectId(id)}
    project ={"_id":0}
    try:
        resultado = mongo.db.departamento.find_one(query, project)
        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# http://127.0.0.1:4000/departamento/porID/<string:id>



@depar.route('/departamento/nuevodepartamento', methods=['POST'])
def add_departamento():
    #from flask import request
    nom   = request.json["nombre"]
    est = request.json["estado"]
    muni   = request.json["municipio"]
    pais  = request.json["pais"]
    num   = request.json["num"]
    dir   = request.json["direccion"]


    if request.method=='POST':
        product={
        "nombre": nom,
        "estado": est,
        "municipio": muni,
        "pais": pais,
        "num": num,
        "direccion": dir
        }


    try:
        resultado = mongo.db.departamento.insert_one(product)
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
    

#http://127.0.0.1:4000/departamento/nuevodepartamento



@depar.route('/departamento/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.departamento.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500
        
        
#http://127.0.0.1:4000/departamento/eliminar/<string:id>



@depar.route('/departamento/actualizar/<string:id>', methods=['PUT'])
def actualizar_departamento(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.departamento.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                return jsonify({"mensaje": "Documento actualizado"})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500


# http://127.0.0.1:4000/departamento/actualizar/<string:id>
    