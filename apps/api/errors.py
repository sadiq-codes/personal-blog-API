# @app.errorhandler(400)
#     def bad_request(error):
#         jsonify({
#             'success': False,
#             'error': 400,
#             'message': "bad request"
#         }), 400
#
#     @app.errorhandler(404)
#     def not_found(error):
#         return jsonify({
#             'success': False,
#             'error': 404,
#             'message': "resource not found"
#         }), 404
#
#     @app.errorhandler(405)
#     def method_not_allowed(error):
#         return jsonify({
#             'success': False,
#             'error': 405,
#             'messsage': 'method not allowed'
#         }), 405
#
#     @app.errorhandler(422)
#     def unprocessable(error):
#         jsonify({
#             'success': False,
#             'error': 422,
#             'message': "unprocessable"
#         }), 422
#
#     @app.errorhandler(500)
#     def not_found(error):
#         jsonify({
#             'success': False,
#             'error': 500,
#             'message': "server error"
#         }), 500
