import gevent
from gevent.monkey import patch_all
patch_all()


from gevent.pywsgi import WSGIServer
import argparse
import socket
import requests
from flask import Flask
from dash.node import LocalNode, RemoteNode


class DashManager():
    def __init__(self):
        self._nodes = {}           # 存储rpc客户端
        self.config = self._load_config_from_cli()

    def _load_config_from_cli(self):
        """
        从终端输入的命令里提取参数
        :return:
        """
        parser = argparse.ArgumentParser(
            description= "一个小巧的linux服务器信息收集服务"
        )

        parser.add_argument(
            '-b', '--bind',
            action='store',
            dest='host',
            default=None,
            metavar='host',
            help='默认 0.0.0.0'
        )

        parser.add_argument(
            '-p', '--port',
            action='store',
            type=int,
            dest='port',
            default=None,
            metavar='port',
            help='监听端口号，默认5000'
        )

        parser.add_argument(
            '-a', '--agent',
            action='store_true',
            dest='agent',
            help='以agent模式启动，开启一个RPC server'
        )

        parser.add_argument(
            '--register-to',
            action='store',
            dest='register_to',
            default=None,
            metavar='host:port',
            help='注册到服务中心，示例: 192.168.30.100:5000'
        )

        return parser.parse_args()

    def run(self):
        if self.config.agent:
            self._run_rpc()
        else:
            self._run_web()

    def _run_rpc(self):
        if not self.config.register_to:
            raise Exception("作为agent必须提供register_to")

        self._init_local_node()     # 初始化本地服务
        self._register_agent()      # 注册agent

        service = self.get_local_node().get_service()
        self.server = zerorpc.Server(service)
        self.server.bind(f'tcp://{self.config.host}:{self.config.port}')
        self.server.run()

    def get_node(self, id):
        return self._nodes.get(id)

    def register_node(self, name, host, port):
        node = RemoteNode(name, host, port)
        node = self.get_node(node.get_id())
        if not node:
            self.add_node(node)

    def get_all_hosts(self):
        hosts = [item.host for item in self._nodes]
        return hosts

    def get_local_node(self):
        return self._nodes.get('localhost')

    def _init_local_node(self):
        self.add_node(LocalNode())

    def add_node(self, node):
        self._nodes[node.get_id()] = node

    def _register_agent(self):
        register_name = socket.gethostname()
        playload = {
            'name': register_name,
            'port': self.config.port
        }

        register_url = f"http://{self.config.register_to}/register"
        res = requests.post(register_url, json=playload)

    def _run_web(self):
        self.app = Flask(__name__)
        self.app.dash_manager = self
        from dash.web import webapi
        self.app.register_blueprint(webapi)

        listen_to = (self.config.host, int(self.config.port))
        self.server = WSGIServer(
            listen_to,
            application=self.app
        )
        self.server.serve_forever()


def main():
    manager = DashManager()
    manager.run()

if __name__ == '__main__':
    main()