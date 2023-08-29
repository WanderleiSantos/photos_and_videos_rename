import os
import datetime
from tkinter.filedialog import askdirectory
from PIL import Image
from pillow_heif import register_heif_opener
import shutil

register_heif_opener()

caminho = askdirectory(title="Selecione uma pasta")
def listar_arquivos(pasta):
    lista_arquivos = []

    for diretorio_atual, subdiretorios, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_completo = os.path.join(diretorio_atual, arquivo)
            local_arquivo = os.path.relpath(caminho_completo, pasta)
            lista_arquivos.append(local_arquivo)

    return lista_arquivos

arquivos_encontrados = listar_arquivos(caminho)

locais = {
    "photos": [".png", ".jpg", ".heic", ".jpeg"],
    "videos": [".mp4", ".mov", ".avi", ".m4v"]
}

for arquivo in arquivos_encontrados:
    nome, extensao = os.path.splitext(f"{caminho}/{arquivo}")
    for pasta in locais:
        if extensao.lower() in locais[pasta]:
            if pasta == "photos":
                img = Image.open(f"{caminho}/{arquivo}")
                img_exif = img.getexif()
                if img_exif.get(306) is None:
                   novo_arquivo = "IMG-" + datetime.datetime.fromtimestamp(os.path.getmtime(f"{caminho}/{arquivo}")).strftime("%Y-%m-%d_%H-%M-%S")
                   datefolder = datetime.datetime.fromtimestamp(os.path.getmtime(f"{caminho}/{arquivo}")).strftime("%Y")
                else:
                   novo_arquivo = "IMG-" + img_exif.get(306).strip().replace(':','-').replace(' ', '_')
                   datastr = img_exif.get(306)
                   datefolder = datastr[0:4]
            else:
                novo_arquivo = "VID-" + datetime.datetime.fromtimestamp(os.path.getmtime(f"{caminho}/{arquivo}")).strftime("%Y-%m-%d_%H-%M-%S")
                datefolder =  datetime.datetime.fromtimestamp(os.path.getmtime(f"{caminho}/{arquivo}")).strftime("%Y")
            if not os.path.exists(f"{caminho}/{pasta}/{datefolder}"):
                os.makedirs(f"{caminho}/{pasta}/{datefolder}")
            shutil.copy(f"{caminho}/{arquivo}",
                      f"{caminho}/{pasta}/{datefolder}/{novo_arquivo}{extensao}")




#print(novo_arquivo)
#print(extensao)
#print(f"{caminho}/{pasta}/{novo_arquivo}{extensao}")
#"IMG-" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")