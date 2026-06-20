import socket
import sys

HOST = "0.0.0.0"

if len(sys.argv) != 2:
    print("Uso: python TCPserver.py porta")
    sys.exit()

PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SCOCK_STREAM)

server.bind((HOST, PORT))
server.listen(5)

print(f"Servidor ouvindo. Porta: {PORT}")
