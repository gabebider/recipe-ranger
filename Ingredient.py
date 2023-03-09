from utils import parseIngredientCore
import spacy
import datetime as dt
class Ingredient():
    def __init__(self, name:str, quantity:str, unit:str,
                nlp:spacy.language.Language):
        assert isinstance(name, str), "Ingredient name must be a string"
        assert isinstance(quantity, str), "Ingredient quantity must be a string"
        assert isinstance(unit, str), "Ingredient unit must be a string"
        assert isinstance(nlp, spacy.language.Language), "nlp must be a spacy language object"

        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.nlp = nlp

        try:
            d = parseIngredientCore(self.name,self.nlp)
            self.core = d["core"]
            self.mods = d["mods"]
        except:
            self.core = None
            self.mods = None
    
    def __str__(self):
        if self.quantity == None and self.unit == None:
            return self.name
        elif self.unit == None:
            return f"{self.quantity} {self.name}"
        elif isinstance(self.unit, list) and isinstance(self.quantity, list):
            return f"{self.quantity[0]} {self.unit[0]} and/of {self.quantity[1]} {self.unit[1]} {self.name}"
        else:
            return f"{self.quantity} {self.unit} {self.name}"

    def setName(self, name):
        self.name = name
        d = parseIngredientCore(self.name,self.nlp)
        self.core = d["core"]
        self.mods = d["mods"]

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setUnit(self, unit):
        self.unit = unit

    def getBreakdown(self):
        return f"{str(self)}\n    Quantity: {self.quantity}\n    Unit: {self.unit}\n    Name: {self.name}\n    Core: {self.core}"
        