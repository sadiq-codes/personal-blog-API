from routes import api
from flask import jsonify


@api.errorhandler(400)
def bad_request(message):
    response = jsonify({'success': False,
                        'error': "Bad Request",
                        'message': message}), 400
    return response


@api.errorhandler(403)
def forbidden(message):
    response = jsonify({'success': False,
                        'error': "Forbidden",
                        'message': message}), 403
    return response


@api.errorhandler(404)
def not_found(message):
    response = jsonify({'success': False,
                        'error': "Resource Not Found",
                        'message': message}), 404
    return response


@api.errorhandler(405)
def method_not_allowed(message):
    response = jsonify({'success': False,
                        'error': "Method Not Allowed",
                        'message': message}), 405
    return response


@api.errorhandler(500)
def not_found(message):
    response = jsonify({'success': False,
                        'error': "Internal Server Error",
                        'message': message}), 500
    return response
