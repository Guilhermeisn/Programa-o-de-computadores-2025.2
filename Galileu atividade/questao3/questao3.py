# 20252014050026 - Guilherme Costa de Albuquerque

import os

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def camDisco(pasta, i):
    return os.path.join(pasta, f"disco{i}.bin")

def inicializaRAID():
    try:
        Pasta = input("Informe a pasta: ").strip()
        nDiscos = int(input("Informe a quantidade de discos: "))
        tamDisco = int(input("Informe o tamanho de cada disco (em bytes): "))
        tamBloco = int(input("Informe o tamanho do bloco (em bytes): "))

        if nDiscos <3:
            raise ValueError("É preciso pelo menos 3 discos. ")
        
        os.makedirs(Pasta, exist_ok=True)
        
        for i in range(nDiscos):
            with open(camDisco(Pasta, i), "wb") as f:
                f.write(b'\x00' * tamDisco)

        print("RAID inicializada com sucesso. ")

        return {
            "Pasta": Pasta,
            "nDiscos": nDiscos,
            "tamDisco": tamDisco,
            "tamBloco": tamBloco
        }
    
    except ValueError as e:
        print("[ERRO]: Erro de valor:", e)
    except Exception as e:
        print("[ERRO]: Ocorreu um erro inesperado:", e)

def obtemRAID():
    try:
        Pasta = input("Informe a pasta: ").strip()
        nDiscos = int(input("Informe a quantidade de discos: "))
        tamDisco = int(input("Informe o tamanho do disco (em bytes): "))
        tamBloco = int(input("Informe o tamanho do bloco (em bytes): "))

        faltando = []
        for i in range(nDiscos):
            if not os.path.exists(camDisco(Pasta, i)):
                faltando.append(i)

        if len(faltando) > 1:
            raise Exception("Mais de um disco está faltando. ")
        print("RAID carregado. ")
        return {
            "Pasta": Pasta,
            "nDiscos": nDiscos,
            "tamDisco": tamDisco,
            "tamBloco": tamBloco,
            "faltando": faltando
            }
        
    except Exception as e:
            print("[ERRO]:", e)

def escreveRAID(cfg):
    try:
        Dados = input("Digite os dados: ").encode()
        Pos = int(input("Posição inicial: "))

        Bloco = cfg["tamBloco"]
        nData = cfg["nDiscos"] - 1

        for i, byte in enumerate(Dados):
            posGlobal = Pos + i
            Stripe = posGlobal // Bloco
            Disco = Stripe % nData
            Offset = (posGlobal % Bloco)

            Caminho = camDisco(cfg["Pasta"], Disco)

            with open(Caminho, "r+b") as f:
                f.seek(Stripe * Bloco + Offset)
                f.write(bytes([byte]))

        atualizarParidade(cfg)
        print("Dados escritos com sucesso. ")

    except Exception as e:
        print("[ERRO]: Erro na escrita: ", e)

def atualizarParidade(cfg):
    try:
        Bloco = cfg["tamBloco"]
        nDiscos = cfg["nDiscos"]
        nData = nDiscos - 1

        Tamanho = cfg["tamDisco"] // Bloco

        for Stripe in range(Tamanho):
            Paridade = b'\x00' * Bloco

            for d in range(nData):
                Caminho = camDisco(cfg["Pasta"], d)
                with open(Caminho, "rb") as f:
                    f.seek(Stripe * Bloco)
                    Dados = f.read(Bloco)
                    Paridade = xor_bytes(Paridade, Dados)

            with open(camDisco(cfg["Pasta"], nData), "r+b") as f:
                f.seek(Stripe * Bloco)
                f.write(Paridade)

    except Exception as e:
        print("[ERRO]: Erro ao atualizar paridade: ", e)
            
def lerRAID(cfg):
    try:
        Pos = int(input("Informe a posição inicial: "))
        Tamanho = int(input("Informe a quantidade de bytes a ler: "))

        Resultado = []
        Bloco = cfg["tamBloco"]
        nData = cfg["nDiscos"] - 1

        for i in range(Tamanho):
            posGlobal = Pos + i
            Stripe = posGlobal // Bloco
            Disco = Stripe % nData
            Offset = (posGlobal % Bloco)

            Caminho = camDisco(cfg["Pasta"], Disco)
            
            if os.path.exists(Caminho):
                with open(Caminho, "rb") as f:
                    f.seek(Stripe * Bloco + Offset)
                    Resultado.append(f.read(1))
            else:
                Valor = reconstruirByte(cfg, Stripe, Offset, Disco)
                Resultado.append(Valor)

        print("Leitura:", b''.join(Resultado).decode(errors="ignore"))

    except Exception as e:
        print("[ERRO]: Erro na leitura: ", e)

def reconstruirByte(cfg, Stripe, Offset, DiscoFaltando):
    Bloco = cfg["tamBloco"]
    nDiscos = cfg["nDiscos"]

    Valor = 0

    for d in range(nDiscos):
        if d == DiscoFaltando:
            continue

        Caminho = camDisco(cfg["Pasta"], d)

        if not os.path.exists(Caminho):
            continue

        with open(Caminho, "rb") as f:
            f.seek(Stripe * Bloco + Offset)
            b = f.read(1)
            if b:
                Valor ^= b[0]

    return bytes([Valor])

def removeDiscoRAID(cfg):
    try:
        Disco = int(input("Informe o disco a remover: "))
        os.remove(camDisco(cfg["Pasta"], Disco))
        print(f"Disco {Disco} removido. ")
    except Exception as e:
        print("[ERRO]:", e)

def reconstroiRAID(cfg):
    try:
        Faltando = [
            i for i in range(cfg["nDiscos"]) 
            if not os.path.exists(camDisco(cfg["Pasta"], i))
        ]

        if len(Faltando) != 1:
            raise Exception("Precisa faltar exatamente um disco para reconstrução. ")
        
        Disco = Faltando[0]
        Bloco = cfg["tamBloco"]
        Tamanho = cfg["tamDisco"] // Bloco

        with open(camDisco(cfg["Pasta"], Disco), "wb") as f_out:
            for Stripe in range(Tamanho):
                Buffer = bytearray(Bloco)
                
                for offset in range(Bloco):
                    Buffer[offset] = reconstruirByte(cfg, Stripe, offset, Disco)[0]

                f_out.write(Buffer)

        print("Disco reconstruído com sucesso!")

    except Exception as e:
        print("[ERRO]: Erro ao reconstruir disco: ", e)
        
def menu():
    cfg = None
    while True:
        print("\nMenu:")
        print("1. Inicializar RAID")
        print("2. Carregar RAID")
        print("3. Escrever no RAID")
        print("4. Ler do RAID")
        print("5. Remover disco do RAID")
        print("6. Reconstruir disco do RAID")
        print("0. Sair")

        Escolha = input("Escolha uma opção: ")

        if Escolha == "1":
            cfg = inicializaRAID()
        elif Escolha == "2":
            cfg = obtemRAID()
        elif Escolha == "3" and cfg:
            escreveRAID(cfg)
        elif Escolha == "4" and cfg:
            lerRAID(cfg)
        elif Escolha == "5" and cfg:
            removeDiscoRAID(cfg)
        elif Escolha == "6" and cfg:
            reconstroiRAID(cfg)
        elif Escolha == "0":
            break
        else:
            print("[ERRO]: RAID não carregado ou opção inválida. ")

if __name__ == "__main__":
    menu()