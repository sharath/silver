from flask import jsonify


def ROOT_STATUS(server, database):
    return jsonify({'server': server, 'database': database})


def REGISTER_ERROR(message):
    return jsonify({'message': message}), 400


def REGISTER_SUCCESS(id, token):
    return jsonify({'id': id, 'token': token})
