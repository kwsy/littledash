import zerorpc
import os
import platform
import psutil
import socket
import time
from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self):
        self._service = None

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def _create_service(self):
        pass

    def get_service(self):
        if not self._service:
            self._service = self._create_service()
        return self._service


class RemoteNode(Node):
    def __init__(self, name, host, port):
        super(RemoteNode, self).__init__()
        self.name = name
        self.host = host
        self.port = int(port)

    def _create_service(self):
        c = zerorpc.Client()
        c.connect(f'tcp://{self.host}:{self.port}')
        return c

    def get_id(self):
        return f"{self.host}"


class LocalNode(Node):
    def __init__(self):
        super(LocalNode, self).__init__()
        self.name = "littledash"

    def get_id(self):
        return 'localhost'

    def _create_service(self):
        return LocalService(self)


class LocalService(object):
    def __init__(self, node):
        self.node = node

    def get_sysinfo(self):
        uptime = int(time.time() - psutil.boot_time())
        sysinfo = {
            'uptime': uptime,
            'hostname': socket.gethostname(),
            'os': platform.platform(),
            'load_avg': os.getloadavg(),
            'num_cpus': psutil.cpu_count()
        }

        return sysinfo