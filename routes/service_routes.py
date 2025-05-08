from flask import Blueprint, jsonify, request
from models.service import Service
from models.db import db
from sqlalchemy.exc import IntegrityError

service = Blueprint('service', __name__)

@service.route('/api/services')
def get_service():
    services = Service.query.all()
    return jsonify([service.serialize() for service in services])

@service.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['description', 'in_date', 'out_date']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")

        new_service = Service(data['description'], data['in_date'], data['out_date'])
        print(f"Creando servicio: {new_service.description}, {new_service.in_date}, {new_service.out_date}")

        db.session.add(new_service)
        db.session.commit()

        return jsonify({'message': 'Servicio agregado exitosamente', 'service': new_service.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'El servicio ya está registrado'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}")
        return jsonify({'error': 'Error al agregar el servicio'}), 500

@service.route("/api/del_service/<int:id>", methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    
    if not service: 
        return jsonify({'message':'Servicio no encontrado'}), 404 
    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Servicio borrado exitosamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@service.route('/api/up_service/<int:id>', methods=['PUT'])
def update_service(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    service = Service.query.get(id)

    if not service:
        return jsonify({'error': 'Servicio no encontrado'}), 404
    
    try:
        if "description" in data:
            service.description = data['description']
        if 'in_date' in data:
            service.in_date = data['in_date']
        if 'out_date' in data:
            service.out_date = data['out_date']

        db.session.commit()

        return jsonify({'message':'Servicio actualizado correctamente', 'service': service.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@service.route('/api/update_service/<int:id>', methods=['PATCH'])
def patch_service(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    service = Service.query.get(id)
    
    if not service:
        return jsonify({'error': 'Servicio no encontrado'}), 404

    try:
        if 'description' in data and data['description']:
            service.description = data['description']
        if 'in_date' in data and data['in_date']:
            service.in_date = data['in_date']
        if 'out_date' in data and data['out_date']:
            service.daout_datete = data['out_date']

        db.session.commit()
        return jsonify({'message': 'Servicio actualizado correctamente', 'service': service.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500