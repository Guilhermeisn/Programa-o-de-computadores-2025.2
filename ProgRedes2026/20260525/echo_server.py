import socket
from config import*

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.bind ((SERVER, PORT))

while True:
    msg, source = my_sock.recvfrom(512)
    my_sock.sendto(msg, source)

my_sock.close()