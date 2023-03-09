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

def get_subtree_text(token):
    """
    Return the text of the subtree rooted at the given token.
    """
    return ' '.join([t.text for t in token.subtree])

def ParseDependency(s):
    """
    Create a dependency parse for the given string and display it in a browser window.
    """
    nlp = spacy.load("en_core_web_trf")
    nlp.add_pipe("merge_compound_and_proper_nouns")
    # nlp.add_pipe("merge_noun_chunks")
    doc = nlp(s)
    html = displacy.render(doc, style="dep",options={"dep":True})
    with open("parse2.html", "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run(["open", "parse2.html"], check=True)

def miniRunner(s):
    # print(s)
    ParseDependency(s)
    # from Instruction import Instruction
    # Instruction(s)
    
if __name__ == '__main__':
    miniRunner("locking tongs")
