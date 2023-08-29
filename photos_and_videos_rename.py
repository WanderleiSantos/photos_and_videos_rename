import os
import datetime
from tkinter.filedialog import askdirectory
from PIL import Image
from pillow_heif import register_heif_opener
import shutil

register_heif_opener()

caminho = askdirectory(title="Selecione uma pasta")

lista_arquivos = os.listdir(caminho)

locais = {
    "photos": [".png", ".jpg", ".heic", ".jpeg"],
    "videos": [".mp4", ".mov", ".avi", ".m4v"]
}

for arquivo in lista_arquivos:
    nome, extensao = os.path.splitext(f"{caminho}/{arquivo}")
    for pasta in locais:
        if extensao in locais[pasta]:
            if pasta == "imagens":
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