from flask import Blueprint, jsonify, request
from models.payment import Payment
from models.db import db
from sqlalchemy.exc import IntegrityError

payment = Blueprint('payment', __name__)

@payment.route('/api/payments')
def get_payment():
    payments = Payment.query.all()
    return jsonify([payment.serialize() for payment in payments])

@payment.route('/api/add_payment', methods=['POST'])
def add_payment():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['cost', 'method', 'date']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:
        print(f"Datos recibidos: {data}")

        new_payment = Payment(data['cost'], data['method'], data['date'])
        print(f"Creando pago: {new_payment.cost}, {new_payment.method}, {new_payment.date}")

        db.session.add(new_payment)
        db.session.commit()

        return jsonify({'message': 'Pago agregado exitosamente', 'payment': new_payment.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'El pago ya está registrado'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error inesperado: {e}")
        return jsonify({'error': 'Error al agregar el pago'}), 500

@payment.route("/api/del_payment/<int:id>", methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get(id)
    
    if not payment: 
        return jsonify({'message':'Pago no encontrado'}), 404 
    try:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({'message': 'Pago borrado exitosamente!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@payment.route('/api/up_payment/<int:id>', methods=['PUT'])
def update_payment(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    payment = Payment.query.get(id)

    if not payment:
        return jsonify({'error': 'Pago no encontrado'}), 404
    
    try:
        if "cost" in data:
            payment.cost = data['cost']
        if 'method' in data:
            payment.method = data['method']
        if 'date' in data:
            payment.date = data['date']

        db.session.commit()

        return jsonify({'message':'Pago actualizado correctamente', 'payment': payment.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@payment.route('/api/update_payment/<int:id>', methods=['PATCH'])
def patch_payment(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    payment = Payment.query.get(id)
    
    if not payment:
        return jsonify({'error': 'Pago no encontrado'}), 404

    try:
        if 'cost' in data and data['cost']:
            payment.cost = data['cost']
        if 'method' in data and data['method']:
            payment.method = data['method']
        if 'date' in data and data['date']:
            payment.date = data['date']

        db.session.commit()
        return jsonify({'message': 'Pago actualizado correctamente', 'payment': payment.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500