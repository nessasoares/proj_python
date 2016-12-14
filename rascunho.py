
es_stopper = u"quem é que quando passa já te deixa tonto, quem é que te coloca e te deixa no ponto, quem é que só de rebolar te enlouqueceu que é? quem é? quem é? a danada sou eu"
#[token.text for token in es_stopper(u"quem é que quando passa já te deixa tonto, quem é que te coloca e te deixa no ponto, quem é que só de rebolar te enlouqueceu que é? quem é? quem é? a danada sou eu")]
#tokenized_documents2 = [ tokenize(di.replace('.','')) for di in es_stopper]

analyzer1 = RegexTokenizer() | LowercaseFilter()
analyzer2 = RegexTokenizer() | LowercaseFilter() | StopFilter(lang="portuguese")

for token in analyzer1(es_stopper):
    print(repr(token.text))

print("--------------------------")
for token in analyzer2(es_stopper):
    print(repr(token.text))
--------------------------------------------------------------------------------------
-------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------
for q in query:
    parsed_query = parser.parse(q)
    try:
        ix = open_dir(index_path)
        with ix.searcher() as searcher:
            results = searcher.search(parsed_query, terms=True)
            print("Found: ",len(results),' documents!')
            if results.has_matched_terms():
                print("All matched terms:",results.matched_terms())
            i = 0
            for ri in results:
                i += 1
                print("document #%d ="%i,' ID:',ri.docnum, ' SCORE:',ri.score)
                print('\t CONTEUDO:',ri['conteudo_full'])
                # Was this results object created with terms=True?
                if results.has_matched_terms():
                    print("\t MATCHED TERMS:",ri.matched_terms())
                else:
                    print()
    finally:
        ix.close()








#parser = QueryParser("conteudo_full", schema)
searcher = ix.searcher()
qp = QueryParser("conteudo_full", schema)
q = qp.parse(u"eu")

with ix.searcher() as s:
    results = s.search(q)
print(results)
