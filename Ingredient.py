from utils import merge_compound_and_proper_nouns
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
    def getMainIngredientBody(ingredientName):
        nlp = spacy.load("en_core_web_md")
        nlp.add_pipe("merge_compound_and_proper_nouns")
        doc = nlp(ingredientName)
        #TODO: implement this function --> should return the text of the noun chunk that is the main ingredient. ex: "the shredded parmesan cheese" should return "parmesan cheese"
        
        
    
    def setName(self, name):
        self.name = name
    
    def setQuantity(self, quantity):
        self.quantity = quantity

    def setUnit(self, unit):
        self.unit = unit

    def getBreakdown(self):
        return f"{str(self)}\n   Quantity: {self.quantity}\n    Unit: {self.unit}\n    Name: {self.name}"
        