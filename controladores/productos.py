from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from app import create_app
from mongo import mongo
from flask import Blueprint, jsonify
from bson.json_util import dumps

prod = Blueprint("products", __name__)
app = create_app()

@prod.route('/productos/get_all', methods=['GET'])
def listar_prod():
    data = mongo.db.productos.find({})#, {"_id":0}
    r = []
    for producto in data:
        producto['_id']= str(producto['_id'])
        r.append(producto)
    return r

#http://127.0.0.1:4000/productos/get_all

@prod.route('/productos/porNombre/<string:nombre>', methods=['GET'])
def obtener_PorNombre(nombre):
    query = {'nombre': {'$eq': nombre}}
    sort = [("nombre", 1)]
    project = {"_id": 0, "nombre": 1, "foto": 1, "clasificacion": 1 ,"precio":1}

    try:
        resultado = mongo.db.productos.find(query, project).sort(sort)
        count_resultado = mongo.db.productos.count_documents(query)

        if count_resultado > 0:
            return dumps(resultado) 
        else:
            return jsonify({"message": "No se encontraron resultados con el nombre"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# #http://127.0.0.1:4000/productos/porNombre/<string:nombre>
    
from bson import ObjectId  # Importa ObjectId del módulo bson

@prod.route('/productos/porId/<string:producto_id>', methods=['GET'])  # Cambia la ruta y el nombre del parámetro
def obtener_PorId(producto_id):
    try:
        # Convierte el ID de cadena a ObjectId
        query = {'_id': ObjectId(producto_id)}
        resultado = mongo.db.productos.find_one(query)

        if resultado:
            # Incluye solo los campos deseados en la respuesta
            datos_respuesta = {
                "_id": str(resultado.get("_id")),
                "foto": resultado.get("foto"),
                "cantidadExistente": resultado.get("cantidadExistente"),
                "nombre": resultado.get("nombre"),
                "precio": resultado.get("precio"),
                "dimensiones": resultado.get("dimensiones")
            }
            return jsonify(datos_respuesta)
        else:
            return jsonify({"message": "No se encontraron resultados con el ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    




@prod.route('/productos/porID/<string:id>' , methods = ['GET'])
def obtener_PorID(id):
    query={'_id': ObjectId(id)}
    project ={"_id":0}
    try:
        resultado = mongo.db.productos.find_one(query, project)
        if resultado: 
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# http://127.0.0.1:4000/productos/porID/<string:id>





@prod.route('/productos/nuevoProd', methods=['POST'])
def add_producto():
    #from flask import request
    n=request.json["nombre"]
    cla=request.json["clasificacion"]["nomClasificacion"]
    des=request.json["clasificacion"]["Descripcion"]


    mod=request.json["modelo"]
    cos=request.json["costo"]
    pre= cos * 1.20

    al=request.json["dimensiones"]["altura"]
    an=request.json["dimensiones"]["ancho"]
    lar=request.json["dimensiones"]["largo"]
    cap=request.json["dimensiones"]["capacidad"]

    num=request.json["numeroDePiezas"]
    col=request.json["color"]
    fot=request.json["foto"]
    



    fechaAdq=request.json["fechaAdquisicion"]

    can=request.json["cantidadExistente"]
    sta=request.json["status"]
    cui=request.json["ciudadanosRecomendados"]
    mat=request.json["materialFabricacion"]
    pas=request.json["paisOrigen"]
    pro=request.json["proveedorId"]
    mar=request.json["marcaId"]
    e=request.json["estado"]
    if request.method=='POST':
        product={
        "nombre": n,
        "clasificacion":{"nomClasificacion":cla,"Descripcion":des},
        "modelo":mod,
        "costo":cos,
        "precio":pre,
        "dimensiones":{"altura":al,"ancho":an, "largo":lar, "capacidad":cap},
        "numeroDePiezas":num,
        "color":col,
        "foto":fot,


        'fechaAdquisicion':fechaAdq,



        "cantidadExistente":can,
        "status":sta,
        "ciudadanosRecomendados":cui,
        "materialFabricacion":mat,
        "paisOrigen":pas,
        "proveedorId":pro,
        "marcaId":[mar, mar, mar],
        "estado": e,
        }

    try:
        resultado = mongo.db.productos.insert_one(product)
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
    

#http://127.0.0.1:4000/productos/nuevoProd




@prod.route('/productos/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
        try:
            resultado = mongo.db.productos.delete_one({'_id':ObjectId(id)})
            if resultado:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "documento eliminado"})
            else:
                # Si no se encuentra el documento, devuelve un mensaje adecuado
                return jsonify({"mensaje": "Documento no encontrado"})
        except Exception as e:
            # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
            return jsonify({"error": str(e)}), 500
        
        
#http://127.0.0.1:4000/productos/eliminar/<string:id>


        

@prod.route('/productos/actualizar/<string:id>', methods=['PUT'])
def actualizar_producto(id):
    campos_actualizar = request.json
    
    try:
        if campos_actualizar:
            resultado = mongo.db.productos.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
            if resultado.modified_count > 0:
                if 'costo' in campos_actualizar:
                    nuevo_costo = float(campos_actualizar['costo'])  # Validar que el costo sea un número
                    nuevo_precio = nuevo_costo * 1.20  # Aumento del 20% al costo
                    mongo.db.productos.update_one({'_id': ObjectId(id)}, {"$set": {"precio": nuevo_precio}})
                return jsonify({"mensaje": "Documento No Actualiza quien sabe por que :("})
            else:
                return jsonify({"mensaje": "Documento no encontrado"}), 404
        else:
            return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
    except ValueError:
        return jsonify({"error": "El costo proporcionado no es un número válido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500


# http://127.0.0.1:4000/productos/actualizar/<string:id>



























# ====================================================================

# # from app import create_app
# # from mongo import mongo
# # from flask import Blueprint , jsonify
# # from bson.json_util import dumps

# # prod = Blueprint("products",__name__)
# # app = create_app()

# # @prod.route('/productos/get_all', methods=['GET'])
# # def listar_prod():
# #     data=mongo.db.productos.find({})
# #     r=dumps(data)
# #     return r


# # @prod.route('/productos/porNombre/<string:nombre>', methods = ['GET'])
# # def obtener_PorNombre(nombre):
# #     #nom=""
# #     query= {'nombre':{'$eq':nombre}}
# #     sort ={("nombre", 1)}
# #     project = {"_id": 0,  "nombre": 1, "precio":1,"dimensiones": 1} 
# #     try:
# #         resultado = mongo.db.productos.find(query,project).sort(sort)
# #         if resultado:
# #             return list(resultado)
# #         else:
# #             return jsonify({"message":"No se encontraron resultados con el nombre "}) ,404
# #     except Exception as e:
# #         return  list({"error": str(e)}) ,500


# from app import create_app
# from mongo import mongo
# from flask import Blueprint, jsonify
# from bson.json_util import dumps

# prod = Blueprint("products", __name__)
# app = create_app()

# @prod.route('/productos/get_all', methods=['GET'])
# def listar_prod():
#     data = mongo.db.productos.find({})
#     r = dumps(data) 
#     return r



# #http://127.0.0.1:4000/productos/get_all

# #---------------------------------------------------------------------------------------------------------------------



# @prod.route('/productos/porNombre/<string:nombre>', methods=['GET'])
# def obtener_PorNombre(nombre):
#     query = {'nombre': {'$eq': nombre}}
#     sort = [("nombre", 1)]
#     project = {"_id": 0, "nombre": 1, "precio": 1, "dimensiones": 1}

#     try:
#         resultado = mongo.db.productos.find(query, project).sort(sort)
#         count_resultado = mongo.db.productos.count_documents(query)

#         if count_resultado > 0:
#             return dumps(resultado) 
#         else:
#             return jsonify({"message": "No se encontraron resultados con el nombre"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500




# #---------------------------------------------------------------------------------------------------------------------




# # #http://127.0.0.1:4000/productos/porNombre/<string:nombre>
    
# from bson import ObjectId  # Importa ObjectId del módulo bson

# @prod.route('/productos/porId/<string:producto_id>', methods=['GET'])  # Cambia la ruta y el nombre del parámetro
# def obtener_PorId(producto_id):
#     try:
#         # Convierte el ID de cadena a ObjectId
#         query = {'_id': ObjectId(producto_id)}
#         resultado = mongo.db.productos.find_one(query)

#         if resultado:
#             # Incluye solo los campos deseados en la respuesta
#             datos_respuesta = {
#                 "nombre": resultado.get("nombre"),
#                 "precio": resultado.get("precio"),
#                 "dimensiones": resultado.get("dimensiones")
#             }
#             return jsonify(datos_respuesta)
#         else:
#             return jsonify({"message": "No se encontraron resultados con el ID"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    



# #---------------------------------------------------------------------------------------------------------------------
    


# @prod.route('/productos/porID/<string:id>' , methods = ['GET'])
# def obtener_PorID(id):
#     query={'_id': ObjectId(id)}
#     project ={"_id":0,"nombre": 1 , "precio": 1, "dimensiones": 1}
#     try:
#         resultado = mongo.db.productos.find_one(query, project)
#         if resultado: 
#             return jsonify(resultado)
#         else:
#             return jsonify({"mensaje": "documento no encontrado"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# #http://127.0.0.1:4000/productos/porID/<string:id>


# #---------------------------------------------------------------------------------------------------------------------

# #INNER JOIN MARCA




# #---------------------------------------------------------------------------------------------------------------------




# #INNER JOIN PROVEEDOR
    
# @prod.route('/productos/prod_prove', methods=['GET'])
# def obtener_prod_prove():
#     query = [
#         {
#             '$lookup': {
#                 'from':"proveedor",
#                 'localField': "provedorId",
#                 'foreignField': "_id",
#                 'as': "proveedor"
#             }
#         },
#         {
#             '$unwind': "$proveedor" # Deshacer el array creado por $lookup
#         },
#         {
#             '$project': {
#                 "_id": 0,
#                 "nombre": 1,
#                 "precio": 1,
#                 "dimenciones": 1,
#                 "proveedor.nombre": 1,
#                 "proveedor.tel": 1,
#                 "proveedor.rfc": 1,
#                 "proveedor.estado": 1
#             }
#         }
#     ]

#     try:
#         resultado = mongo.db.productos.aggregate(query)
#         if resultado:
#         # Si la consulta es exitosa, devuelve los datos en formato JSON
#             return list(resultado)
#         else:
#         # Si no se encuentra el documento, devuelve un mensaje adecuado
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#     # Manejo de la excepción, puedes personalizar el mensaje de error según tus
#     # necesidades
#         return jsonify({"error": str(e)}), 500


# #http://127.0.0.1:4000/productos/prod_prove
    


# #---------------------------------------------------------------------------------------------------------------------




# #INNER JOIN PROVEEDOR
    
# @prod.route('/productos/prod_paisOrig', methods=['GET'])
# def obtener_prod_paisOrig():
#     query = [
#         {
#             '$lookup': {
#                 'from':"pais de origen",
#                 'localField': "paisOrigen",
#                 'foreignField': "_id",
#                 'as': "paisOrigen"
#             }
#         },
#         {
#             '$unwind': "$paisOrigen" # Deshacer el array creado por $lookup
#         },
#         {
#             '$project': {
#                 "_id": 0,
#                 "nombre": 1,
#                 "precio": 1,
#                 "dimenciones": 1,
#                 "paisOrigen.noombre": 1,
#                 "paisOrigen.estado": 1,
#                 "paisOrigen.municipio": 1,
#                 "paisOrigen.cp": 1,
#             }
#         }
#     ]

#     try:
#         resultado = mongo.db.productos.aggregate(query)
#         if resultado:
#         # Si la consulta es exitosa, devuelve los datos en formato JSON
#             return list(resultado)
#         else:
#         # Si no se encuentra el documento, devuelve un mensaje adecuado
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
#     except Exception as e:
#     # Manejo de la excepción, puedes personalizar el mensaje de error según tus
#     # necesidades
#         return jsonify({"error": str(e)}), 500


# #http://127.0.0.1:4000/productos/prod_paisOrig



# from app import create_app
# from mongo import mongo
# from flask import Blueprint , jsonify
# from bson.json_util import dumps

# prod = Blueprint("products",__name__)
# app = create_app()

# @prod.route('/productos/get_all', methods=['GET'])
# def listar_prod():
#     data=mongo.db.productos.find({})
#     r=dumps(data)
#     return r


# @prod.route('/productos/porNombre/<string:nombre>', methods = ['GET'])
# def obtener_PorNombre(nombre):
#     #nom=""
#     query= {'nombre':{'$eq':nombre}}
#     sort ={("nombre", 1)}
#     project = {"_id": 0,  "nombre": 1, "precio":1,"dimensiones": 1} 
#     try:
#         resultado = mongo.db.productos.find(query,project).sort(sort)
#         if resultado:
#             return list(resultado)
#         else:
#             return jsonify({"message":"No se encontraron resultados con el nombre "}) ,404
#     except Exception as e:
#         return  list({"error": str(e)}) ,500



    # product1={"nombProd":"lampara de mano",
    # "caracteristicas":"['led','40 wats', 'para interior']",
    # "categoria":{"categoria":"consumibles","descripcion":"material para limpieza"},
    # "unidadMedida":"pza",
    # "foto":"foco.jpg",
    # "estatus":"activo",
    # "paisOrigen":"Alemania",
    # "cantidadExistente":123,
    # "costo":200,
    # "precio":220,
    # #'fechaAdquisicion': datetime.strptime(fecha_str, "%d/%m/%Y").date(),
    # "fechaCreación": datetime.now(),
    # "prov_id":1,
    # "marca_id":1}





# @prod.route('/productos/actualizar/<string:id>', methods=['PUT'])
# def actualizar_costo(id):
#     nuevo_costo =request.json["costo"]
    
#     try:
#         resultado = mongo.db.productos.update_one({'_id':ObjectId(id)},{"$set": {"costo": nuevo_costo}})
#         if resultado:
#             actualizar_precio(id, nuevo_costo)
#             return jsonify({"mensaje": "Documento actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"}), 404
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# def actualizar_precio(id, nuevo_costo):
#     try:
#         resultado = mongo.db.productos.update_one({'_id':ObjectId(id)},{"$set": {"precio": nuevo_costo + (nuevo_costo*20/100)}})
#         if resultado:
#             return jsonify({"mensaje": "Precio actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"})
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# def actualizar_precio(id, nuevo_costo):
#     try:
#         resultado = mongo.db.productos.update_one({'_id':ObjectId(id)},{"$set": {"precio": nuevo_costo + (nuevo_costo*20/100)}})
#         if resultado:
#             return jsonify({"mensaje": "Precio actualizado"})
#         else:
#             return jsonify({"mensaje": "Documento no encontrado"})
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    

# #http://127.0.0.1:4000/productos/actualizar/<string:id>



# @prod.route('/productos/actualizar/<string:id>', methods=['PUT'])
# def actualizar_producto(id):
#     campos_actualizar = request.json
    
#     try:
#         if campos_actualizar:
#             resultado = mongo.db.productos.update_one({'_id': ObjectId(id)}, {"$set": campos_actualizar})
#             if resultado.modified_count > 0:
#                 # Si el campo 'costo' está presente, actualiza el precio
#                 if 'costo' in campos_actualizar:
#                     actualizar_precio(id, campos_actualizar['costo'])
#                 return jsonify({"mensaje": "Documento actualizado"})
#             else:
#                 return jsonify({"mensaje": "Documento no encontrado"}), 404
#         else:
#             return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # http://127.0.0.1:4000/productos/actualizar/<string:id>