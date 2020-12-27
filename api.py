import os
import ast
import _ast
import inspect
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

host = '0.0.0.0'
port = 8000


def inspect_module(module_path):
    with open(module_path) as mf:
        tree = ast.parse(mf.read())
    module_classes = [_ for _ in tree.body if isinstance(_, _ast.ClassDef)]
    module_classes = [(cls.name, [_.name for _ in cls.body if isinstance(_, _ast.FunctionDef)]) for cls in
                      module_classes]
    return module_classes


script_path = os.path.dirname(os.path.abspath(__file__))
working_space = os.path.basename(script_path)

modules = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__)) + '/apps') if
           f.endswith('.py') and not f.startswith('__')]

app = Flask(__name__)
CORS(app)

app.secret_key = 'ReActor2019!1..'
handle_exceptions = app.handle_exception
handle_user_exception = app.handle_user_exception
app.handle_user_exception = handle_exceptions
app.handle_user_exception = handle_user_exception
api = Api(app)

print('Static Endpoints:')
i = 1
for module in modules:
    module_name = os.path.splitext(module)[0]
    class_name = inspect_module('apps/' + module)[0][0]
    m = __import__('apps.' + module_name, globals(), locals(), class_name)
    import_module = inspect.getmembers(m)
    new_key = None
    for key, value in import_module:
        if class_name == key:
            new_key = [x for x, y in enumerate(import_module) if y[0] == key]
    import_module_name = import_module[new_key[0]]
    c = getattr(m, import_module_name[0])
    if '_' in module_name:
        module_name = module_name.replace('_', '')
    route = '/api/' + module_name
    print(str(i) + ' : ' + 'http://' + host + ':' + str(port) + route)
    i += 1
    api.add_resource(c, route)


@app.errorhandler(400)
def bad_request(error):
    code = 400
    response = {'success': False, 'code': code, 'message': str(error)}
    return jsonify(data=response), code


@app.errorhandler(403)
def forbidden(error):
    code = 403
    response = {'success': False, 'code': code, 'message': str(error)}
    return jsonify(data=response), code


@app.errorhandler(404)
def page_not_found(error):
    code = 404
    response = {'success': False, 'code': code, 'message': str(error)}
    return jsonify(data=response), code


@app.errorhandler(405)
def method_not_allowed(error):
    code = 405
    response = {'success': False, 'code': code, 'message': str(error)}
    return jsonify(data=response), code


@app.errorhandler(500)
def internal_error(error):
    code = 500
    response = {'success': False, 'code': code, 'message': str(error)}
    return jsonify(data=response), code


@app.after_request
def add_header(response):
    response.headers['X-Powered-By'] = 'Ante-JamNet/1.1.0'
    response.headers['Server'] = 'JamNet/1.1.0'
    response.headers['X-Server'] = 'JamNet/1.1.0'
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Origin', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST,GET,OPTIONS,PUT,DELETE,HEAD,PATCH')

    return response


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True, threaded=True, use_reloader=True)
