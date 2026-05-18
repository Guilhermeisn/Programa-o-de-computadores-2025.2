# 20252014050026 - Guilherme Costa de Albuquerque

import sys
import socket
import struct

if len(sys.argv) !=2:
    print("Uso: python questao2.py <arquivo.pcap>")
    sys.exit(1)

try:
    f = open(sys.argv[1], 'rb')

except FileNotFoundError:
    print("[ERRO]: Arquivo não encontrado.")
    sys.exit(1)

except PermissionError:
    print("[ERRO]: Você não tem permissão para acessar o arquivo.")
    sys.exit(1)

except Exception as e:
    print("[ERRO]: Ocorreu um erro inesperado.")
    sys.exit(1)

except FileNotFoundError:
    print("[ERRO]: Arquivo não encontrado!")
    sys.exit(1)

MAC = lambda b: ':'.join(f'{x:02x}' for x in b)
with f:

    HDR = f.read(24)
    Magic = int.from_bytes(HDR[:4], 'big')

    if Magic == 0xA1B2C3D4:
        Endian, div = 'big', 1_000_000
    elif Magic == 0xD4C3B2A1:
        Endian, div = 'little', 1_000_000
    elif Magic == 0xA1B23C4D:
        Endian, div = 'big', 1_000_000_000
    elif Magic == 0x4D3CB2A1:
        Endian, div = 'little', 1_000_000_000
    else:
        print("PCAP inválido.")
        sys.exit(1)

    TempoInc = None
    TempoFim = None
    Trafego = {}
    Pacote = 0

    while True:
        PH = f.read(16)
        if len(PH) < 16:
            break

        Pacote += 1

        Sec = int.from_bytes(PH[0:4], Endian)
        Usec = int.from_bytes(PH[4:8], Endian)

        Tempo = Sec + (Usec / div)

        if TempoInc is None:
            TempoInc = Tempo

        TempoFim = Tempo

        Tam = int.from_bytes(PH[8:12], Endian)
        Dados = f.read(Tam)

        if len(Dados) < 34:
            continue

        dstMAC, srcMac, ETH = struct.unpack('!6s6sH', Dados[:14])

        if ETH != 0x0800:
            continue

        IP = Dados[14:34]
        vihl, tos, total, ident, frag, ttl, proto, chk, src, dst = \
            struct.unpack('!BBHHHBBH4s4s', IP)
        
        Versao = vihl >> 4
        IHL = (vihl & 15) * 4

        if Versao != 4:
            continue

        srcIP = socket.inet_ntoa(src)
        dstIP = socket.inet_ntoa(dst)

        Trafego[srcIP] = Trafego.get(srcIP, 0) + total
        Trafego[dstIP] = Trafego.get(dstIP, 0) + total

        print(f'\n=== Pacote {Pacote} ===')
        print(f'MAC: {MAC(srcMac)} -> {MAC(dstMAC)}')
        print(f'TTL: {ttl} | Total: {total} | ID: {ident} | Frag: {frag}')
        print(f'IP: {srcIP} -> {dstIP}')

        Payload = Dados[14 + IHL:]

        if proto == 1 and len(Payload) >= 8:
            Tipo = Payload[0]

            Nomes = {
                0: 'Echo Reply',
                3: 'Destination Unreachable',
                5: 'Redirect',
                8: 'Echo Request',
                11: 'Time Exceeded',
            }

            print(f'ICMP: {Nomes.get(Tipo, Tipo)}')
            if Tipo in (0, 8):
                ident = int.from_bytes(Payload[4:6], 'big')
                seq = int.from_bytes(Payload[6:8], 'big')
                print(f'Identificação: {ident}')
                print(f'Sequência: {seq}')

        elif proto == 6 and len(Payload) >= 20:
            srcp, dst_p, seq, ack, off_flags, win, chk, urg = \
                struct.unpack('!HHLLHHHH', Payload[:20])
            Flags = off_flags & 0x01FF

            nomes = {
                1: 'FIN',
                2: 'SYN',
                4: 'RST',
                8: 'PSH',
                16: 'ACK',
                32: 'URG',
                64: 'ECE',
                128: 'CWR',
            }

            ativos = [n for b, n in nomes.items() if Flags & b]

            print(f'TCP: {srcp} -> {dst_p}')
            print(f'SEQ: {seq} | ACK: {ack}')
            print(f'WIN: {win} | FLAGS: {ativos}')

        elif proto == 17 and len(Payload) >= 8:
            srcp, dst_p = struct.unpack('!HH', Payload[:4])
            print(f'UDP: {srcp} -> {dst_p}')

print('Estatísticas:')

if Trafego:
    IP = max(Trafego, key=Trafego.get)
    print(f'IP com mais tráfego: {IP}')
    print(f'Bytes transferidos: {Trafego[IP]}')

if TempoInc is not None and TempoFim is not None:
    print(f'Intervalo de captura: {(TempoFim - TempoInc):.6f} segundos')