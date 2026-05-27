import socket
from config import*

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_ip = socket.gethostbyname(socket.gethostname())
my_sock.bind ((my_ip, PORT))
print (f"Escutando em ({my_ip}:{PORT})")

while True:
    msg, source = my_sock.recvfrom(512)
    print (f"Recebi/devolvendo a {source}: {msg}")
    my_sock.sendto(msg, source)

my_sock.close()