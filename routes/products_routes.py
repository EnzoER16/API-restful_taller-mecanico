from flask import Blueprint, jsonify, request
from models.products import Products
from models.db import db
from sqlalchemy.exc import IntegrityError

product = Blueprint('products', __name__)

@product.route('/api/products')
def get_products():
    products = Products.query.all()
    return jsonify([product.serialize() for product in products])

@product.route('/api/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['productName', 'price', 'stock']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")

        new_product = Products(data['productName'], data['price'], data['stock'])
        print(f"Creando producto: {new_product.productName}, {new_product.price}, {new_product.stock}")

        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Producto agregado exitosamente', 'product': new_product.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'El producto ya está registrado'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}")
        return jsonify({'error': 'Error al agregar el producto'}), 500

@product.route("/api/del_product/<int:id>", methods=['DELETE'])
def delete_product(id):
    product = Products.query.get(id)
    
    if not product: 
        return jsonify({'message':'Producto no encontrado'}), 404 
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Producto borrado exitosamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@product.route('/api/up_product/<int:id>', methods=['PUT'])
def update_product(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    product = Products.query.get(id)

    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    try:
        if 'name' in data:
            product.productName = data['productName']
        if 'email' in data:
            product.price = data['price']
        if 'stock' in data:
            product.stock = data['stock']

        db.session.commit()

        return jsonify({'message':'Producto actualizado correctamente', 'product': product.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@product.route('/api/update_product/<int:id>', methods=['PATCH'])
def patch_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    product = Products.query.get(id)
    
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404

    try:
        if 'productName' in data and data['productName']:
            product.productName = data['productName']
        if 'price' in data and data['price']:
            product.price = data['price']
        if 'stock' in data and data['stock']:
            product.stock = data['stock']

        db.session.commit()
        return jsonify({'message': 'Producto actualizado correctamente', 'product': product.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500