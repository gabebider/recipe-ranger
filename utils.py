import spacy
from spacy import displacy
from spacy.language import Language
import subprocess

@Language.component("merge_compound_and_proper_nouns")
def merge_compound_and_proper_nouns(doc):
    """
    Create spacy factory component to merge compound and proper nouns, but not adjectives or determinants. This should mean that it identifies "parmesan cheese" as a single noun, but not "the shredded parmesan cheese".
    """
    with doc.retokenize() as retokenizer:
        for np in doc.noun_chunks:
            if any(tok.pos_ in ["PROPN", "NOUN"] for tok in np):
                boolArray = [tok.pos_ in ["PROPN", "NOUN"] for tok in np]
                startIdx = boolArray.index(True)
                endIdx = len(boolArray) - boolArray[::-1].index(True)
                retokenizer.merge(np[startIdx:endIdx])
    
    for np in doc.noun_chunks:
        boolArray = [tok.pos_ in ["PROPN", "NOUN"] for tok in np]
        assert boolArray.count(True) <= 1, "More than one noun after noun chunks merged"

    return doc

def get_dependent_nouns(head_token):
    dependent_nouns = []
    for token in head_token.doc:
        if token.head == head_token:
            if token.pos_ in ['PROPN', 'NOUN']:
                dependent_nouns.append(token.txt)
            else:
                dependent_nouns += get_dependent_nouns(token)
    return dependent_nouns

def print_noun_phrases(s):
    """
    Print the noun phrases in the given string.
    """
    nlp = spacy.load("en_core_web_md")
    # nlp.add_pipe("merge_compound_and_proper_nouns")
    doc = nlp(s)
    print(f"Noun phrases in '{s}':")
    for np in doc.noun_chunks:
        print(np.text)
    print()

def ParseDependency(s):
    """
    Create a dependency parse for the given string and display it in a browser window.
    """
    nlp = spacy.load("en_core_web_trf")
    nlp.add_pipe("merge_compound_and_proper_nouns")
    doc = nlp(s)
    html = displacy.render(doc, style="dep",options={"dep":True})
    with open("parse2.html", "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run(["open", "parse2.html"], check=True)

def miniRunner(s):
    ParseDependency(s)
    # print_noun_phrases(s)
    
link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

if __name__ == '__main__':
    miniRunner("Bring a large pot of lightly salted water to a boil")
    miniRunner("Cook orzo until al dente, 8 to 10 minutes.")
    miniRunner("Drain and rinse with cold water.")
    miniRunner("When orzo is cool, transfer to a medium bowl and mix in olives, feta cheese, parsley, dill, and tomato.")
    miniRunner("Whisk together oil and lemon juice in a small bowl.")
    miniRunner("Pour over orzo mixture; mix well.")
    miniRunner("Season with salt and pepper; chill before serving.")