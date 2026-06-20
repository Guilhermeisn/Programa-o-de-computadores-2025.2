import socket

server = socket.socket(socket.AF_INETM, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 5000))

print("Servidor UDP iniciado")