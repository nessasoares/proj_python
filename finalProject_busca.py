#imports
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from pprint import pprint
from whoosh.fields import Schema, TEXT

#busca
busca = input("Busca:")
query = busca.split(" ")
print(query)

try:
    schema = Schema(titulo=TEXT(stored=True),
                conteudo_tkn=TEXT(stored=True),
                conteudo_full=TEXT(stored=True))
    parser = QueryParser("conteudo_tkn", schema)
    myquery = parser.parse("eu OR você")

    ix = open_dir("whoosh_index")
    with ix.searcher() as searcher:
        results = searcher.search(myquery, terms=True)
        print("Retrieved: ",len(results),' documents!')
        for ri in results:
            print('score:',ri.score, 'of document:',ri.docnum)
except:
    ix.close()

print("Search: done. :D")
