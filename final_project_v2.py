#imports
import numpy as np

file_path = "obras_machado_assis/README"
linhas = []
arquivos = []
categorias = ("contos", "critica", "cronica", "miscelanea", "poesia", "romance", "teatro", "traducao")

file = {
        "path": file_path,
        "linhas" : linhas,
        "arquivos" : arquivos,
        "full_text" : "",
}
with open(file_path, 'r', encoding = "ISO-8859-1") as arquivo:
    file["full_text"] = arquivo.readlines()

#file["linhas"] = file["full_text"].split('\n')

print(file["full_text"])
