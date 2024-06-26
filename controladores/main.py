from app import create_app
from productos import prod
from proveedores import prove
from marca import marc
from carrito import carrito

app = create_app()
app.register_blueprint(prod)
app.register_blueprint(prove)
app.register_blueprint(marc)
app.register_blueprint(carrito)
if __name__=="__main__":
    app.run( host="0.0.0.0", port=4000, debug=True)
    
    
