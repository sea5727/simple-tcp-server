import errno
import queue
import socket
import select
import sys

PORT=12345

class ServerSocket:
    def __init__(self, mode, port, read_callback, max_connections, recv_bytes):
        if mode == 'localhost':
            self.ip = mode
        elif mode == 'public':
            self.ip = socket.gethostname()
        else:
            self.ip = mode
        
        self.port = port

        if type(self.port) != int:
            pinrt("port must be an int", file=sys.stderr)
            raise ValueError
    
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setblocking(0)
        self._socket.bind((self.ip, self.port))
        self.callback = read_callback
        self._max_connections = max_connections
        if type(self._max_connections) != int:
            print("max_connections must be an int", file=sys.stderr)
            raise ValueError
    
        self.recv_bytes = recv_bytes
    def run(self):
        self._socket.listen(self._max_connections)
        readers = [self._socket]
        writers = []
        queues = dict()

        IPs = dict()
        while readers:
            read, write, err = select.select(readers, writers, readers)
            for sock in read:
                if sock is self._socket:
                    client_socket, client_ip = self._socket.accept()
                    client_socket.setblocking(0)
                    readers.append(client_socket)
                    queues[client_socket] = queue.Queue()
                    IPs[client_socket] = client_ip
                    print('client accept..:{}'.format(client_ip))
                else:
                    try:
                        data = sock.recv(self.recv_bytes)
                    except socket.error as e:
                        if e.errno == errno.ECONNRESET:
                            data = None
                        else:
                            raise e
                    if data:
                        self.callback(IPs[sock], queues[sock], data)
                        if sock not in writers:
                            writers.append(sock)
                    else:
                        if sock in writers:
                            writers.remove(sock)
                        readers.remove(sock)
                        sock.close()
                        del queues[sock]

            for sock in write:
                try:
                    data = queues[sock].get_nowait()
                except queue.Empty:
                    writers.remove(sock)
                else:
                    sock.send(data)
            
            for sock in err:
                readers.remove(sock)
                if sock in writers:
                    writers.remove(sock)
                sock.close()
                del queues[sock]



def echo(ip, queue, data):
    queue.put(data)
    

server = ServerSocket('localhost', 12345, echo, 5, 2000)
server.run()

