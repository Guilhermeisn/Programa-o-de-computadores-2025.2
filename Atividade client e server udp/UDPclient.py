import socket

Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = input("Digite uma mensagem: ")

Client.sendto(msg.encode(), ("127.0.0.1", 5000))

data, addr = Client.recvfrom(1024)

print("Resposta do servidor:", data.decode())

Client.close()