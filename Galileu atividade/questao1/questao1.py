# 20252014050026 - Guilherme Costa de Albuquerque

import subprocess

def listaJPEG(directory):

    try:
        Resultado = subprocess.run(
            ["cmd", "/c", "dir", "/b", directory],
            capture_output=True,
            text=True
        )

        Arquivos = Resultado.stdout.splitlines()
        arqJPEG = [
            f"{directory}\\{Arq}"
            for Arq in Arquivos
            if Arq.lower().endswith((".jpg", ".jpeg"))
        ]

        return arqJPEG
    
    except subprocess.CalledProcessError:
        print("[ERRO]: Não foi possível acessar o diretório.")
        return []
    
    except FileNotFoundError:
        print("[ERRO]: Diretório não encontrado.")
        return []
    
    except Exception as Erro:
        print(f"[ERRO]: Um erro inesperado aconteceu.")
        return []
    
def dataGPS(camImagem):

    try:
        Resultado = subprocess.run(
            ["C:\\Users\\adm\\Downloads\\exiftool-13.58_64\\exiftool.exe",
            "-GPSLatitude",
            "-GPSLongitude",
            "-n",
            camImagem],
            capture_output=True,
            text=True
        )

        Latitude = None
        Longitude = None

        for Linha in Resultado.stdout.splitlines():

            if "GPS Latitude" in Linha:
                Latitude = float(Linha.split(":")[1].strip())

            elif "GPS Longitude" in Linha:
                Longitude = float(Linha.split(":")[1].strip())

        if Latitude is not None and Longitude is not None:
            return (Latitude, Longitude)
            
    except FileNotFoundError:
        print("[ERRO]: O exiftool não foi encontrado.")

    except  ValueError:
        print(f"[ERRO]: Erro ao converter os dados da imagem: {camImagem}")

    except subprocess.CalledProcessError:
        print(f"[ERRO]: Erro ao processar a imagem: {camImagem}")

    except Exception as Erro:
        print(f"[ERRO]: Um erro inesperado aconteceu: {Erro}")

    return None
    
def encontrarGPS(directory):

    Coordenadas = []

    Arquivos = listaJPEG(directory)

    for Arq in Arquivos:
        GPS = dataGPS(Arq)

        if GPS:
            Coordenadas.append(GPS)

        if len(Coordenadas) == 10:
            break

    return Coordenadas
    
def googleMapsURL(Coordenadas):
    if not Coordenadas:
        return "Não foi encontrada nenhuma coordenada."
    
    URL = "https://www.google.com/maps/dir/"

    for Latitude, Longitude in Coordenadas:
        URL += f"{Latitude},{Longitude}/"

    return URL.rstrip("/")

def main():

    try:

        directory = input("Digite o caminho do diretório: ")

        Coordenadas = encontrarGPS(directory)

        if not Coordenadas:
            print("Nenhuma imagem com GPS encontrada.")
            return
    
        URL = googleMapsURL(Coordenadas)

        print("\nRota gerada:")
        print(URL)

    except KeyboardInterrupt:
        print("\nO programa foi interrompido.")
    
    except Exception as Erro:
        print(f"[ERRO]: Um erro inesperado ocorreu no programa: {Erro}")

if __name__ == "__main__":
    main()