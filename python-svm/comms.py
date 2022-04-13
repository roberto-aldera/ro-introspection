# comms
import socket
HOST = '127.0.0.1'
PORT = 12345

def receive(conn):
    data = b''
    word = b''
    while word != b'\n':
        data += word
        word = conn.recv(1)
    message = data.decode('utf-8')
    return message

def send(msg, sock):
    message = msg + '\n'
    sock.sendall(message.encode('utf-8'))

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((HOST, PORT))
# s.listen(1)
# conn, addr = s.accept()

# print("connesso")

# data_to_send = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# for i in range(10):
#     send(data_to_send[i], conn)
#     print(receive(conn))