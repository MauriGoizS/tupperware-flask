from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

emple = Blueprint("empleado", __name__)
app = create_app()



@emple.route('/empleado/get_all', methods=['GET'])
def listar_empleado():
    data = mongo.db.empleado.find({})
    r = []
    for empleado in data:
        empleado['_id']=str(empleado['_id'])
        r.append(empleado)
    return r

#http://127.0.0.1:4000/empleado/get_all




@emple.route('/empleado/porGmail/<string:gmail>', methods=['GET'])
def obtener_PorGmail(gmail):
    query = {'gmail': {'$eq': gmail}}
    sort = [("gmail", 1)]
    project = {"_id": 0, "gmail": 1, "foto": 1}

    try:
        resultado = mongo.db.empleado.find(query, project).sort(sort)
        count_resultado = mongo.db.empleado.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el gmail"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #http://127.0.0.1:4000/empleado/porgmail/<string:nombre>



@emple.route('/empleado/porID/<string:id>' , methods = ['GET'])
def obtener_PorID(id):
    query={'_id': ObjectId(id)}
    project ={"_id":0}
    try:
        resultado = mongo.db.empleado.find_one(query, project)
        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# http://127.0.0.1:4000/empleado/porID/<string:id>



@emple.route('/empleado/nuevoempleado', methods=['POST'])
def add_empleado():
    #from flask import request
    gma   = request.json["gmail"]
    passw = request.json["password"]
    sta   = request.json["status"]
    edad  = request.json["edad"]
    fot   = request.json["foto"]
    dir   = request.json["direccion"]


    if request.method=='POST':
        product={
        "gmail": gma,
        "password": passw,
        "status": sta,
        "edad": edad,
        "foto":fot,
        "direccion": dir
        }


    try:
        resultado = mongo.db.empleado.insert_one(product)
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
    

#http://127.0.0.1:4000/empleado/nuevoempleado



@emple.route('/empleado/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.empleado.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500
        
        
#http://127.0.0.1:4000/empleado/eliminar/<string:id>



@emple.route('/empleado/actualizar/<string:id>', methods=['PUT'])
def actualizar_empleado(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.empleado.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                return jsonify({"mensaje": "Documento actualizado"})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500


# http://127.0.0.1:4000/empleado/actualizar/<string:id>
    