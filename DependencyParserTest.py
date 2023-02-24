import spacy
from spacy import displacy

def test():
    nlp = spacy.load('en_core_web_sm')
    doc = nlp("1 (.25 ounce) package active dry yeast")
    print("Parse head:",doc[0].head)
    displacy.serve(doc, style='dep', auto_select_port=True)
    

if __name__ == '__main__':
    test()