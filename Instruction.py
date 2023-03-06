import spacy
from utils import get_subtree_text
from Parse import Parse
import re
class Instruction:
    def __init__(self,text):
        self.text = text
        self.parse_text()
        #! remove this: printing for debugging
        for parse in self.parses:
            print("Parse: ")
            print(self.parses[parse])
            print()

    def __str__(self):
        return self.text
    
    def parse_text(self):
        nlp = spacy.load("en_core_web_trf")
        doc = nlp(self.text)
        root = list(doc.sents)[0].root
        action_verbs = [root]
        

        def get_action_verbs(token):
            # recursively get all verbs attached by "conj" to the root verb
            for child in token.children:
                if child.dep_ == "conj" and child.pos_ == "VERB":
                    action_verbs.append(child)
                    get_action_verbs(child)

        get_action_verbs(root)

        def generate_parse(head_token):
            parse_verb = head_token.text
            dobjs = []
            modifiers = []
            for token in head_token.children:
                subtree_text = get_subtree_text(token)
                if token.dep_ == "dobj":
                    dobjs.append(get_subtree_text(token))
                elif token.dep_ == "prep" and token.pos_ == "ADP":
                    if re.search(r"(?i)boil(ing)?", subtree_text):
                        modifiers.append(("until", "boiling"))
                    elif token.text.lower() == "until":
                        modifiers.append(("until", subtree_text))
                    elif re.search(r"(minutes?)|(hours?)|(seconds?)", subtree_text):
                        modifiers.append(("time", subtree_text))
                elif token.dep_ == "npadvmod" and re.search(r"(minutes?)|(hours?)|(seconds?)", subtree_text):
                    modifiers.append(("time", subtree_text))

            return Parse(parse_verb, dobjs, modifiers)
        
        parses = {}
        for verb in action_verbs:
            parses[verb.text] = generate_parse(verb)
        
        self.parses = parses
            
       
        
        


    
