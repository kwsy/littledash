import gevent
from gevent.monkey import patch_all
patch_all()


from gevent.pywsgi import WSGIServer
import argparse


class DashManager():
    def __init__(self):
        self.rpc_clients = {}           # 存储rpc客户端
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
        print('rpc')

    def _run_web(self):
        print('web')


def main():
    manager = DashManager()
    manager.run()

if __name__ == '__main__':
    main()