from flask import Blueprint, request, jsonify, current_app


webapi = Blueprint('littledash', __name__)


@webapi.route("/hosts")
def hosts():
    all_host = current_app.dash_manager.get_all_hosts()
    return jsonify(all_host)


@webapi.route("/<str:host>/system_info")
def system_info(host):
    service = current_app.dash_manager.get_node(host).get_service()
    info = service.get_sysinfo()
    return jsonify(info)


@webapi.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    port = data['port']
    host = request.remote_addr
    current_app.dash_manager.register_node(name, host, port)
