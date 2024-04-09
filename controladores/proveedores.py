from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

prove = Blueprint("proveedors", __name__)
app = create_app()



@prove.route('/proveedor/get_all', methods=['GET'])
def listar_prove():
    data = mongo.db.proveedor.find({})
    r = []
    for proveedor in data:
        proveedor['_id']=str(proveedor['_id'])
        r.append(proveedor)
    return r
    

#http://127.0.0.1:4000/proveedor/get_all





@prove.route('/proveedor/porNombre/<string:nombre>', methods=['GET'])
def obtener_ProNombre(nombre):
    query = {'nombre': {'$eq': nombre}}
    sort = [("nombre", 1)]
    project = {"_id": 0, "nombre": 1, "tel": 1, "rfc": 1}

    try:
        resultado = mongo.db.proveedor.find(query, project).sort(sort)
        count_resultado = mongo.db.proveedor.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el nombre"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# #http://127.0.0.1:4000/proveedor/porNombre/<string:nombre>
    


@prove.route('/proveedor/porID/<string:id>' , methods = ['GET'])
def obtener_ProID(id):
    query={'_id': ObjectId(id)}
    project ={"_id":0,"nombre": 1 , "tel": 1, "rfc": 1 ,"estado":1}
    try:
        resultado = mongo.db.proveedor.find_one(query, project)
        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# http://127.0.0.1:4000/proveedor/porID/<string:id>
    






@prove.route('/proveedor/nuevoProd', methods=['POST'])
def add_proveedor():
    #from flask import request
    n=request.json["nombre"]
    tel=request.json["tel"]
    rfc= request.json["rfc"]
    est=request.json["estado"]





    if request.method=='POST':
        product={
        "nombre": n,
        "tel": tel,
        "rfc":rfc,
        "estado":est
        }


    try:
        resultado = mongo.db.proveedor.insert_one(product)
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
    

#http://127.0.0.1:4000/proveedor/nuevoProd
    
@prove.route('/proveedor/actualizar/<string:id>', methods=['PUT'])
def actualizar_proveedor(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.proveedor.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                return jsonify({"mensaje": "Documento actualizado"})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500

#http://127.0.0.1:4000/proveedor/actualizar/<string:id>


@prove.route('/proveedor/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.proveedor.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500

#http://127.0.0.1:4000/productos/eliminar/65cfaa6003ba538c29738fbd