from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.local import LocalProxy


webapi = Blueprint('littledash', __name__)


def get_current_node():
    return current_app.dash_manager.get_node(g.host)


def get_current_service():
    return get_current_node().get_service()


current_node = LocalProxy(get_current_node)
current_service = LocalProxy(get_current_service)


@webapi.before_request
def get_host():
    g.host = request.args.get('host', 'localhost')


@webapi.route("/hosts")
def hosts():
    all_host = current_app.dash_manager.get_all_hosts()
    return jsonify(all_host)


@webapi.route("/system_info")
def system_info():
    info = current_service.get_sysinfo()
    return jsonify(info)


@webapi.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    port = data['port']
    host = request.remote_addr
    current_app.dash_manager.register_node(name, host, port)
    return jsonify({'status': 0})
