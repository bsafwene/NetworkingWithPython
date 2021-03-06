import argparse, socket

def recvall(sock, length):
    data=b''
    while len(data) < length:
        more = sock.recv(length-len(data))
        if not more:
            raise EOFError('was expecting {d} byets but only received'
                           ' {d} bytes before the socket closed'.format(length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('listening at', sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('socket name:', sc.getsockname())
        print('socket peer:', sc.getpeername())
        message = recvall(sc, 16)
        print('  Incoming sixteen bytes message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print('  Reply sent, socket closed')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))

if __name__ == '__main__':
    choices = {'client' : client, 'server':server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which rol to play')
    parser.add_argument('host', help='interface the server listens at;'
                                     ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(def=1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
