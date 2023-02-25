import spacy
from spacy import displacy
from recipe_scrapers import scrape_me
import textacy

str1 = "dried bread crumbs, seasoned"
str2 = "all-purpose flour"

def getIngredientRoot(s=str1):
    nlp = spacy.load('en_core_web_sm')
    # add merge noun chunks to the pipeline
    nlp.add_pipe('merge_noun_chunks')
    doc = nlp(s)
    assert len(list(doc.sents)) == 1, "There should be only one sentence in the ingredient"
    root = list(doc.sents)[0].root
    print("Parse root:",root)
    print(list(root.children))
    # displacy.serve(doc, style='dep', auto_select_port=True)
    
link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

def splitSteps(lnk=link):
    scraper = scrape_me(lnk)
    steps = scraper.instructions()
    steps = steps.replace("\n", "")
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(steps)
    
    print("Sentences:")
    for sent in doc.sents:
        assert sent != None, "Sentence is None"
        print(sent)

if __name__ == '__main__':
    # getIngredientRoot()
    splitSteps()