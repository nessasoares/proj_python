# imports
import numpy as np
import os.path
import re
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.lang import languages
from whoosh.analysis import StopFilter, RegexTokenizer, LowercaseFilter, StemmingAnalyzer
from stop_words import get_stop_words
from whoosh.qparser import QueryParser

#functions
def text_treat(path):
    conto = {
            "titulo":"",
            "categoria":"",
            "texto":[],
            "ano":"",
            "full":[],
            "tokens":[]
    }
    with open(path, 'r', encoding = "ISO-8859-1") as arquivo:
        conto["full"] = arquivo.readlines()

    analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="portuguese")
    #exemplo: Poesia, Americanas, 1875

    p = re.compile(r'[/.,]')
    inf = p.split(conto["full"][0])
    #inf = conto["full"][0].split(r"[/.,]")
    conto["categoria"] = inf[0]
    conto["titulo"] = inf[1]
    conto["ano"] = inf[2].replace("\n", "")

    for i in range(len(conto["full"])):
        conto["texto"].append(conto["full"][i].replace('\n', ''))

        #retirar stop words
        for token in analyzer(conto["texto"][i]):
            conto["tokens"].append(token.text)
        #conto["tokens"] = remove_stop_words(conto["texto"][i])
    return conto
#---------------------------------------------------------------------
def remove_stop_words(str):
    analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="portuguese")
    r = []
    for token in analyzer(str):
        r.append(token.text)
    return r

#---------------------------------------------------------------------


#variaveis
arqs = []
categorias = ("contos", "critica", "cronica", "miscelanea", "poesia", "romance", "teatro", "traducao")
stop_words = get_stop_words('portuguese')
analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="portuguese")
index_path = "whoosh_index"
print("------------------------------------------------------------------------------")
print("----------------------------buscador da vava----------------------------------")
print("------------------------------------------------------------------------------\n\n\n")
#Schema
#criar só com conteudo, depois separo as informações
schema = Schema(caminho=TEXT,
                titulo=TEXT(stored=True),
                ano = TEXT,
                categoria = TEXT,
                tokens=TEXT(stored=True),
                body=TEXT(analyzer=StemmingAnalyzer()),
                url=TEXT
                )

if not os.path.exists(index_path):
    os.mkdir(index_path)
ix = create_in(index_path, schema)
ix.close()

action = input("Arquivos ja foram indexados? (y|n)")

if action == "n":
    print("\nIndexando os arquivos...")
    # leitura de arquivo
    readme_path = "obras_machado_assis/CONTENTS"

    with open(readme_path, 'r', encoding = "ISO-8859-1") as arquivo:
        readme = arquivo.readlines()

    file = {
            "nome_arquivo": readme_path,
            "texto": "".join(readme),
            "linhas": [],
            "arquivos": [],
            }

    obra = {
            "titulo":"",
            "categoria":"",
            "texto":[],
            "ano":"",
            "full":[],
            "tokens":[]
    }
    # lendo os caminhos dos arquivos
    for i in range(len(readme)):
        aux = readme[i].replace('\n', '')
        file["linhas"].append(aux.lower().split('\n'))
        if aux.lower() not in categorias:
            arqs.append(aux)

    arqs = [i for i in arqs if i != '']
    arqs.pop(0)

    for x in range(len(arqs)):
        aux = arqs[x].split(' ')
        file["arquivos"].append(aux[0].replace(':', ''))

    #indexando os arquivos
    try:
        ix = open_dir("whoosh_index")
        writer = ix.writer()
        #ler os arquivos com os contos
        for x in range(len(file["arquivos"])):
            path = 'obras_machado_assis/'+file["arquivos"][x]
            obra = text_treat(path)
            print(obra["titulo"])
            url = "http://machado.mec.gov.br/images/stories/html/"+file["arquivos"][x]
            print(url)
            writer.add_document(caminho=path,
                                tokens=obra["tokens"],
                                body=obra["full"],
                                titulo = obra["titulo"],
                                ano = obra["ano"],
                                categoria = obra["categoria"],
                                url=url
                                )
            #writer.add_document(titulo ="path", tokens=["primeiro", "segundo"], body="cheap thrills")
            #writer.add_document(titulo =path, tokens=["shawn", "selena", "sia"], body="segundo teste")
        writer.commit()
    finally:
        ix.close()

    print("Indexing: done. :D")

#---------------------------------------------------------------------------
#---------------------------------------BUSCA ------------------------------

action = input("Deseja buscar? (y|n)")
if action == 'y':
    busca = input("O que deseja buscar? ")
    b = remove_stop_words(busca)
    query = ' OR '.join(b)
    print(query)
    try:
        qp = QueryParser("tokens", schema)
        q = qp.parse(query)
        ix = open_dir(index_path)

        with ix.searcher() as searcher:
            results = searcher.search(q, terms=True)
            print("Resultado: ",len(results),' obras!')
            for ri in results:
                print(ri['url'])
                print(ri['url'])
            print()
    except:
        ix.close()

    print("\nSearch: done. :D")

#-----------------------------------------------------------------------------------------------------
