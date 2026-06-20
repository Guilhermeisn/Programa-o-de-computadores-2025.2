import socket
import sys

if len(sys.argv) != 4:
    print("Uso: python TCPclient.py host porta mensagem")
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
MENSAGEM = sys.argv[3]

