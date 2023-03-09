from utils import get_subtree_text, merge_compound_and_proper_nouns
import spacy
class Ingredient():
    def __init__(self, name="[ENTER NAME]", quantity="[ENTER QUANTITY]", unit="[ENTER UNIT]"):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    
    def __str__(self):
        if self.quantity == None and self.unit == None:
            return self.name
        elif self.unit == None:
            return f"{self.quantity} {self.name}"
        elif isinstance(self.unit, list) and isinstance(self.quantity, list):
            return f"{self.quantity[0]} {self.unit[0]} and/of {self.quantity[1]} {self.unit[1]} {self.name}"
        else:
            return f"{self.quantity} {self.unit} {self.name}"
        
    @staticmethod
    def parseIngredientCore(ingredientName:str):
        """
        Parses the ingredient name and returns the core ingredient and modifiers, in the form of a dictionary.

        Parameters:
            ingredientName (str): The ingredient name to be parsed.

        Returns:
            dict: A dictionary containing the core ingredient and modifiers.
        """
        # TODO: make these more efficient --> somehow pass around doc or span objects
        nlp = spacy.load("en_core_web_trf")
        nlp.add_pipe("merge_compound_and_proper_nouns")
        doc = nlp(ingredientName)

        # TODO: test this with temperature and time -- right now just returns the first noun
        np = list(doc.noun_chunks)[0]
        core = None
        for token in np:
            # print(token.text,token.pos_)
            if token.pos_ in ["PROPN","NOUN"]:
                core = token
                break

        if core == None:
            print("getMainIngredientBody: No noun found in ingredient name, returning None")
            return None  
            
        mods = []
        for child in core.children:
            if child.dep_ in ["amod","appos"]:
                mods.append(get_subtree_text(child))
                #! temp debug
                print(child.text,child.dep_,child.pos_,child.tag_)
        
        return {"core":core.text,"mods":mods}
                
    def setName(self, name):
        self.name = name
        d = Ingredient.parseIngredientCore(self.name)
        self.core = d["core"]
        self.mods = d["mods"]

    
    def setQuantity(self, quantity):
        self.quantity = quantity

    def setUnit(self, unit):
        self.unit = unit

    def getBreakdown(self):
        return f"{str(self)}\n    Quantity: {self.quantity}\n    Unit: {self.unit}\n    Name: {self.name}\n    Core: {self.core}"
        