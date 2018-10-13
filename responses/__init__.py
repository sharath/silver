from flask import jsonify


def ROOT_STATUS(server, database):
    return jsonify({'server': server, 'database': database})


def REGISTER_ERROR_USER():
    return jsonify({'message': 'USER_TAKEN'}), 409


def REGISTER_ERROR_PASSWORD():
    return jsonify({'message': 'PASSWORD_TOO_SHORT'}), 409


def REGISTER_ERROR_EMAIL():
    return jsonify({'message': 'INVALID_EMAIL'}), 409


def REGISTER_SUCCESS(id, token):
    return jsonify({'id': id, 'token': token})


def LOGIN_SUCCESS(id, token):
    return jsonify({'id': id, 'token': token})


def LOGIN_ERROR():
    return jsonify({'message': "INVALID_CREDENTIALS"}), 400


def TOKEN_ERROR():
    return jsonify({'message': "TOKEN_INVALID"}), 400
