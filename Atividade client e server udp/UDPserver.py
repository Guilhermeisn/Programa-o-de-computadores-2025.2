import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 5000))

print("Servidor UDP iniciado")

while True:
    data, addr = server.recvfrom(1024)

    print("Recebdo: ", data.decode())
    server.sendto(b"Mensagem recebida", addr)