import os
import datetime
from tkinter.filedialog import askdirectory
from PIL import Image
from pillow_heif import register_heif_opener
import shutil

register_heif_opener()

def listar_arquivos(pasta):
    lista_arquivos = []

    for diretorio_atual, subdiretorios, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_completo = os.path.join(diretorio_atual, arquivo)
            local_arquivo = os.path.relpath(caminho_completo, pasta)
            lista_arquivos.append(local_arquivo)

    return lista_arquivos


def obter_nome_novo_arquivo(caminho_origem, arquivo, pasta_sync):
    caminho_arquivo = os.path.join(caminho_origem, arquivo)
    data_modificacao = datetime.datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
    if pasta_sync == "photos":
        return retorna_novo_nome_arquivo_foto(caminho_arquivo, data_modificacao)
    else:
        return retorna_novo_nome_arquivo_video(data_modificacao)


def retorna_novo_nome_arquivo_foto(caminho_arquivo, data_modificacao):
    img = Image.open(caminho_arquivo)
    img_exif = img.getexif()

    if img_exif and img_exif.get(306):
        novo_arquivo = "IMG-" + img_exif.get(306).strip().replace(':', '-').replace(' ', '_')
        data_str = img_exif.get(306)
    else:
        novo_arquivo = "IMG-" + data_modificacao.strftime("%Y-%m-%d_%H-%M-%S")
        data_str = data_modificacao.strftime("%Y-%m-%d %H:%M:%S")
    year_folder = data_str[:4]

    return novo_arquivo, year_folder

def retorna_novo_nome_arquivo_video(data_modificacao):
    novo_arquivo = "VID-" + data_modificacao.strftime("%Y-%m-%d_%H-%M-%S")
    year_folder = data_modificacao.strftime("%Y")

    return novo_arquivo, year_folder



def main():
    print("Processando arquivos...")
    caminho_origem = askdirectory(title="Selecione uma pasta")
    caminho_destino = "C:/Users/Wanderlei Santos/OneDrive/Imagens/PhotoSync"
    arquivos_encontrados = listar_arquivos(caminho_origem)

    locais = {
        "photos": [".png", ".jpg", ".heic", ".jpeg"],
        "videos": [".mp4", ".mov", ".avi", ".m4v"]
    }

    for arquivo in arquivos_encontrados:
        nome_arquivo, extensao = os.path.splitext(arquivo)
        for pasta, extensoes in locais.items():
            if extensao.lower() in extensoes:
                novo_arquivo, year_folder = obter_nome_novo_arquivo(caminho_origem, arquivo, pasta)
                destino = os.path.join(caminho_destino, pasta, year_folder)
                print(destino)
                if not os.path.exists(destino):
                    os.makedirs(destino)
                    print(f"=== Criando pasta  {destino} ===")
                destino_arquivo = os.path.join(destino, f"{novo_arquivo}{extensao}")
                shutil.copy(os.path.join(caminho_origem, arquivo), destino_arquivo)
                print(f"Arquivo {arquivo} copiado para {destino_arquivo}")

    print("Processamento concluído!")

if __name__ == "__main__":
    main()