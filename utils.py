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

@Language.component("merge_hyphenated_tokens")
def merge_hyphenated_tokens(doc):
    """
    Create spacy factory component to merge hypenated tokens into one token
    """
    with doc.retokenize() as retokenizer:
        for token in doc[1:-1]:
            print(token.text)
            if token.text.endswith('-') and doc[token.i+1].text and doc[token.i-1].text:
                retokenizer.merge(doc[token.i-1:token.i+2])
    return doc


def parseIngredientCore(ingredientName:str, nlp:spacy.language.Language):
    """
    Parses the ingredient name and returns the core ingredient and modifiers, in the form of a dictionary.

    Parameters:
        ingredientName (str): The ingredient name to be parsed.

    Returns:
        dict: A dictionary containing the core ingredient and modifiers.
    """
    assert isinstance(ingredientName, str), "Ingredient name must be a string"
    assert isinstance(nlp, spacy.language.Language), "nlp must be a spacy language object"

    EMPTY_RETURN = {"core": None,"descriptors":[],"preparations":[]}

    # TODO: make these more efficient --> somehow pass around doc or span objects instead of re-parsing every time
    doc = nlp(ingredientName)

    # TODO: test this with temperature and time -- right now just returns the first noun
    try:
        np = list(doc.noun_chunks)[0]
    except: 
        return EMPTY_RETURN
    
    core = None
    for token in np:
        # print(token.text,token.pos_)
        if token.pos_ in ["PROPN","NOUN"]:
            core = token
            break

    if core == None:
        print("getMainIngredientBody: No noun found in ingredient name, returning None")
        return EMPTY_RETURN
        
    descriptors = []
    preparations = []

    for child in core.children:
        if child.dep_ in ["amod","appos","acl","relcl"]:
            if child.tag_ == "JJ":
                if child.text[-2:] == "ed":
                    preparations.append(child.text)
                else:
                    descriptors.append(get_subtree_text(child))
            elif child.tag_ == "VBN":
                preparations.append(get_subtree_text(child))
            else:
                print("getMainIngredientBody: Unhandled adjective/participle type:",child.text,child.tag_)
        elif child.tag_ == "JJ":
            if child.text[-2:] == "ed":
                print("parseIngredientCore: adding adj to preparations without correct dependency:",child.text)
                preparations.append(child.text)
            else:
                print("parseIngredientCore: adding adj to descriptors without correct dependency:",child.text)
                descriptors.append(child.text)
        elif child.tag_ == "VBN":
            print("parseIngredientCore: adding participle to preparations without correct dependency:",child.text)
            preparations.append(child.text)
    
    return {"core":core.text,"descriptors":descriptors,"preparations":preparations}

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
    nlp.add_pipe("merge_hyphenated_tokens")
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

def runMultiple(arr):
    for s in arr:
        miniRunner(s)

orzo_ingredients = ["uncooked orzo pasta",
                    "pitted green olives",
                    "diced feta cheese",
                    "chopped fresh parsley",
                    "chopped fresh dill",
                    "ripe tomato, chopped",
                    "virgin olive oil",
                    "lemon juice",
                    "salt and pepper to taste"]

orzo_2 = ["onion, chopped","garlic, minced","lemon, zested","lemon, sliced for garnish"]
    
if __name__ == '__main__':
    miniRunner("long-grain rice")

# TODO: modify parsing code so that it will read something like "salt and pepper to taste" as two separate ingredients
# -- "salt to taste" and "pepper to taste"