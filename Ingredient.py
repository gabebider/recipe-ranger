
class Ingredient():
    def __init__(self, name="[ENTER NAME]", quantity="[ENTER QUANTITY]", unit="[ENTER UNIT]"):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    
    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"
    
    def setName(self, name):
        self.name = name
    
    def setQuantity(self, quantity):
        self.quantity = quantity

    def setUnit(self, unit):
        self.unit = unit

    def printBreakdown(self):
        return f"{self.quantity} {self.unit} {self.name}\n   Quantity: {self.quantity}\n    Unit: {self.unit}\n    Name: {self.name}"