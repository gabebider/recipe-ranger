import spacy
from spacy import displacy
from spacy.tokens import Token
from spacy.language import Language
import subprocess
import os
# this file is my first born child -- Eli

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

    doc = nlp(ingredientName)

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
        elif child.tag_ == "JJ":
            if child.text[-2:] == "ed":
                preparations.append(child.text)
            else:
                descriptors.append(child.text)
        elif child.tag_ == "VBN":
            preparations.append(child.text)
    
    return {"core":core.text,"descriptors":descriptors,"preparations":preparations}

def get_subtree_text(token):
    """
    Return the text of the subtree rooted at the given token.
    """
    return ' '.join([t.text for t in token.subtree])

def get_obj_text(token):
    """
    Return the text of the token with amods and advmods attached
    """
    remove_tokens_by_deps(token, {"cc","ccomp","prep"})
    if token._.trimmed_subtree == None:
        return token.text
    return ' '.join([t.text for t in token._.trimmed_subtree if t.dep_ in ["amod","advmod","dobj","pobj","nsubj","conj"]])


def remove_tokens_by_deps(token, deps_to_remove):
    """
    Remove all tokens that have a specified set of dependency labels from the
    token's subtree, and create a new custom attribute called 'trimmed_subtree'
    for the token that contains the subtree with the specified dependencies
    removed.
    
    Args:
        token (spacy.tokens.Token): The token to remove dependencies from.
        deps_to_remove (set): A set of dependency labels to remove.
    
    Returns:
        None
    """
    trimmed_children = set()
    processed_children = set()

    def remove_all_children(token):
        for child in token.children:
            if child not in processed_children:
                trimmed_children.add(child)
                processed_children.add(child)
                remove_all_children(child)

    def trim_children(token):
        for child in token.children:
            if child not in processed_children:
                if child.dep_ in deps_to_remove:
                    remove_all_children(child)
                else:
                    processed_children.add(child)
                    trim_children(child)

    trim_children(token)
    token._.trimmed_subtree = [t for t in token.subtree if t not in trimmed_children]

def get_conjuncts(tokens, processed=None):
    """
    Recursively adds all objects connected to another object by the dependency relation "conj" into a list.
    """
    if processed is None:
        processed = set()
    conjuncts = set()
    for token, idx in tokens:
        if token not in processed:
            processed.add(token)
            conjuncts |= set([(t,idx) for t in token.subtree if t.dep_ == "conj"])
    if conjuncts:
        conjuncts |= get_conjuncts(conjuncts, processed=processed)
    return tokens | conjuncts

def ParseDependency(s):
    """
    Create a dependency parse for the given string and display it in a browser window.
    """
    nlp = spacy.load("en_core_web_trf")
    nlp.add_pipe("merge_hyphenated_tokens")
    nlp.add_pipe("merge_compound_and_proper_nouns")

    doc = nlp(s)
    html = displacy.render(doc, style="dep",options={"dep":True})
    with open("parse.html", "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run(["open", "parse.html"], check=True)

def miniRunner(s):
    print(s)
    ParseDependency(s)
    # from Instruction import Instruction
    # Instruction(s)

def runMultiple(arr):
    for s in arr:
        miniRunner(s)
    os.system("rm parse.html")

# some arrays for testing
orzo_ingredients = ["uncooked orzo pasta",
                    "pitted green olives",
                    "diced feta cheese",
                    "chopped fresh parsley",
                    "chopped fresh dill",
                    "ripe tomato, chopped",
                    "virgin olive oil",
                    "lemon juice",
                    "salt and pepper to taste"]

orzo_instructions = [
    "Bring a large pot of lightly salted water to a boil.",
    "Cook orzo until al dente, 8 to 10 minutes.",
    "Drain and rinse with cold water",
    "When orzo is cool, transfer to a medium bowl and mix in olives, feta cheese, parsley, dill, and tomato.",
    "Whisk together oil and lemon juice in a small bowl.",
    "Pour over orzo mixture.",
    "mix well.",
    "Season with salt and pepper.",
    "chill before serving.",
]

orzo_2 = ["onion, chopped","garlic, minced","lemon, zested","lemon, sliced for garnish"]
    
def add_to_tools(list_of_tools):
    # helper function used to exntend the list of tools in tools.txt
    tool_set = set()

    with open("tools.txt","r") as f:
        tool = f.read()
        tool_set.add(tool.strip())

    tool_set |= set(list_of_tools)

    with open("tools.txt","w") as f:
        for tool in tool_set:
            f.write(tool.strip() + "\n")

if __name__ == '__main__':
    # Token.set_extension("trimmed_subtree", default=None, force=True)
    miniRunner("Bring a large pot of lightly salted water to a boil")
    # add_to_tools(["pot", "wok", "saucepan", "knife", "cutting board", "spoon", "fork", "plate", "bowl", "cup", "mug", "blender", "toaster", "microwave", "oven", "mixing bowl", "measuring cup", "colander", "strainer", "grater", "peeler", "tongs", "ladle", "whisk", "rolling pin", "can opener", "bottle opener", "corkscrew", "dish rack", "dish soap", "sponge"]

