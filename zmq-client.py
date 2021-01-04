import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect('tcp://127.0.0.1:5000')
socket.connect('tcp://127.0.0.1:6000')

for i in range(10):
    msg = bytes('msg {}'.format(i), 'UTF-8')
    socket.send(msg)
    print('[Send] {}'.format(msg))
    msg_in = socket.recv()
    print('[Recv] {}'.format(msg_in))