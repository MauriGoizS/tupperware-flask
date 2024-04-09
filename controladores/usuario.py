from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

usua = Blueprint("usuario", __name__)
app = create_app()



@usua.route('/usuario/get_all', methods=['GET'])
def listar_usua():
    data = mongo.db.usuario.find({})
    r = []
    for usuario in data:
        usuario['_id']=str(usuario['_id'])
        r.append(usuario)
    return r

#http://127.0.0.1:4000/usuario/get_all




@usua.route('/usuario/porGmail/<string:gmail>', methods=['GET'])
def obtener_PorGmail(gmail):
    query = {'gmail': {'$eq': gmail}}
    sort = [("gmail", 1)]
    project = {"_id": 0, "gmail": 1, "foto": 1}

    try:
        resultado = mongo.db.usuario.find(query, project).sort(sort)
        count_resultado = mongo.db.usuario.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el gmail"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #http://127.0.0.1:4000/usuario/porgmail/<string:nombre>



@usua.route('/usuario/porID/<string:id>' , methods = ['GET'])
def obtener_PorID(id):
    query={'_id': ObjectId(id)}
    project ={"_id":0}
    try:
        resultado = mongo.db.usuario.find_one(query, project)
        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# http://127.0.0.1:4000/usuario/porID/<string:id>



@usua.route('/usuario/nuevoUsuario', methods=['POST'])
def add_usuario():
    #from flask import request
    gma   = request.json["gmail"]
    passw = request.json["password"]
    rol   = request.json["rol"]
    fot   = request.json["foto"]


    if request.method=='POST':
        product={
        "gmail": gma,
        "password": passw,
        "rol":rol,
        "foto":fot
        }


    try:
        resultado = mongo.db.usuario.insert_one(product)
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
    

#http://127.0.0.1:4000/usuario/nuevoUsuario



@usua.route('/usuario/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.usuario.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500
        
        
#http://127.0.0.1:4000/usuario/eliminar/<string:id>



@usua.route('/usuario/actualizar/<string:id>', methods=['PUT'])
def actualizar_usuario(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.usuario.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                return jsonify({"mensaje": "Documento actualizado"})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500


# http://127.0.0.1:4000/usuario/actualizar/<string:id>
    