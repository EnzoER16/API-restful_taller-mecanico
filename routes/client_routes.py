from flask import Blueprint, jsonify, request
from models.client import Client
from models.db import db
from sqlalchemy.exc import IntegrityError

client = Blueprint('client', __name__)

@client.route('/api/clients')
def get_client():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients])

@client.route('/api/add_client', methods=['POST'])
def add_client():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['name', 'email', 'phone']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")

        new_client = Client(data['name'], data['email'], data['phone'])
        print(f"Creando cliente: {new_client.name}, {new_client.email}, {new_client.phone}")

        db.session.add(new_client)
        db.session.commit()

        return jsonify({'message': 'Cliente agregado exitosamente', 'client': new_client.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'El cliente ya está registrado'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}")
        return jsonify({'error': 'Error al agregar el cliente'}), 500

@client.route("/api/del_client/<int:id>", methods=['DELETE'])
def delete_client(id):
    client = Client.query.get(id)
    
    if not client: 
        return jsonify({'message':'Cliente no encontrado'}), 404 
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Cliente borrado exitosamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@client.route('/api/up_client/<int:id>', methods=['PUT'])
def update_cliente(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    client = Client.query.get(id)

    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    
    try:
        if "name" in data:
            client.name = data['name']
        if 'email' in data:
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']

        db.session.commit()

        return jsonify({'message':'Cliente actualizado correctamente', 'client': client.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@client.route('/api/update_client/<int:id>', methods=['PATCH'])
def patch_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    client = Client.query.get(id)
    
    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        if 'name' in data and data['name']:
            client.name = data['name']
        if 'email' in data and data['email']:
            client.email = data['email']
        if 'phone' in data and data['phone']:
            client.phone = data['phone']

        db.session.commit()
        return jsonify({'message': 'Cliente actualizado correctamente', 'client': client.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500