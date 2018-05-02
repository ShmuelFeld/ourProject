#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.corpora import WikiCorpus
from mywikicorpus import MyWikiCorpus
inp = "../hewiki-latest-pages-articles.xml.bz2"

outp = "wiki.he.text"
i = 0
def hebCarOrSpace(x):
    if( u"\u0590" <= x <= u"\u05EA"):
        return True
    elif(x.isdigit()):
        return True
    elif(x.isspace()):
        return True
    elif(x=="'"):
        return True
    return False
def hebCar(x):
    if( u"\u0590" <= x <= u"\u05EA"):
        return True
    return False
print("Starting to create wiki corpus")
output = open(outp, 'w')
space = " "
wiki = MyWikiCorpus(inp)
# wiki = WikiCorpus(inp, lemmatize=False, dictionary={})

for text in wiki.get_texts():
    # for t in text:
    #     print(t)
    # print(text)

    article = space.join(text)
    m = article.replace(". ", '\n').replace(", ", " ").replace("-", " ").replace(":", " ")
    n = filter(lambda x: hebCarOrSpace(x), m)
    # for arti in article
    output.write("{}\n".format(n.encode("utf-8")))
    i += 1
    if (i % 1000 == 0):
        print("Saved " + str(i) + " articles")
output.close()
print("Finished - Saved " + str(i) + " articles")
