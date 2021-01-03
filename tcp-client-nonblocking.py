import sys
import socket

class ClientSocket:
    def __init__(self, mode, port, recv_bytes=2048, single_use=True):
        if mode == 'localhost':
            self.connect_ip = mode
        elif mode == 'public':
            self.connect_ip = socket.gethostname()
        else:
            self.connect_ip = mode
        
        self.connect_port = port
        if type(self.connect_port) != int:
            print('Port must be an integer!', file=sys.stderr)
            raise ValueError

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_bytes = recv_bytes
        self.single_use = single_use
        if not self.single_use:
            self._socket.connect((self.connect_ip, self.connect_port))
            self.closed = False
        
        self.used = False
    
    def send(self, data):
        if self.single_use:
            if self.used:
                print("You cannot use a single-use socket twice", file=sys.stderr)
                raise RuntimeError
        
            self._socket.connect((self.connect_ip, self.connect_port))
            self.closed = False

        if type(data) == str:
            data = bytes(data, 'UTF-8') # TODO
        
        if type(data) != bytes:
            print('Data must be a string or bytes', file=sys.stderr)
            raise ValueErorr

        print('[Send]{}'.format(data))
        self._socket.send(data)
        self.used = True
        response = self._socket.recv(self.recv_bytes)
        print('[Recv]{}'.format(response))

        if self.single_use:
            self._socket.close()
            self.closed = True
        return response


client = ClientSocket('localhost', 12345)
client.send('sendtestdata')