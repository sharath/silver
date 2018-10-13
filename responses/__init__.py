from flask import jsonify


def ROOT_STATUS(server, database):
    return jsonify({'server': server, 'database': database})


def REGISTER_ERROR(message):
    return jsonify({'message': message})


def REGISTER_SUCCESS(id, token):
    return jsonify({'id': id, 'token': token})


def LOGIN_SUCCESS(id, token):
    return jsonify({'id': id, 'token': token})


def LOGIN_ERROR():
    return jsonify({'message': "INVALID_CREDENTIALS"}), 400
