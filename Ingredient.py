
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
    
    def setName(self, name):
        self.name = name
    
    def setQuantity(self, quantity):
        self.quantity = quantity

    def setUnit(self, unit):
        self.unit = unit

    def getBreakdown(self):
        return f"{str(self)}\n   Quantity: {self.quantity}\n    Unit: {self.unit}\n    Name: {self.name}"