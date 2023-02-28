import requests
from bs4 import BeautifulSoup
from Ingredient import Ingredient
from recipe_scrapers import scrape_me
import re

class Recipe():
    def __init__(self, url, ingredients = {}, instructions = []):
        self.url = url
        self.ingredients: list[Ingredient] = ingredients
        self.instructions = instructions
    
    def addIngredient(self, ingredient):
        self.ingredients[ingredient.name] = ingredient

    def addInstruction(self, instruction):
        self.instructions.append(instruction)

    def getIngredientsFromUrl(self):
        soup = BeautifulSoup(requests.get(self.url).text, "html.parser")
        ingredients_section = soup.find('ul', {'class': 'mntl-structured-ingredients__list'})
        ingredients_list = ingredients_section.find_all('li')

        for ingredient in ingredients_list:
            sections = ingredient.find_all("span")
            newIngredient = Ingredient()
            for section in sections:
                if 'data-ingredient-quantity' in section.attrs:
                    newIngredient.setQuantity(section.text.strip())
                elif 'data-ingredient-unit' in section.attrs:
                    newIngredient.setUnit(section.text.strip())
                elif 'data-ingredient-name' in section.attrs:
                    newIngredient.setName(section.text.strip())

            self.addIngredient(newIngredient)
    
    def parseForIngredients(self):
        scraper = scrape_me(self.url)
        ingList = scraper.ingredients()

        # Define regular expressions for amount and unit
        amountRe = r'\d+(?:\.\d+)?-\d+(?:\.\d+)?|\d+(?:\.\d+)?/\d+|\d+(?:\.\d+)?\s+\d+/\d+|\d+(?:\.\d+)?\s+\d+(?:\.\d+)?(?!-)|\d+(?:\.\d+)?'
        unitRe = r'\b(?<!-)[a-zA-Z]+\b'

        # Iterate over each entry in the array and extract information
        for ingredient in ingList:
        # Extract amount, unit, and ingredient using regular expressions
            amount = re.search(amountRe, ingredient)
            unit = re.search(unitRe, ingredient)
            # If no amount is given, ingredient is just the item
            if amount == None:
                name = ingredient
                amount = None
                unit = None
            # Checks if found unit is a valid unit
            else:
                unitRegex = r'(?i)\b(package[s]?|mm|millimeter[s]?|millimetre[s]?|cm|centimeter[s]?|centimetre[s]?|m|meter[s]?|metre[s]?|inch[es]?|in|yard[s]?|mg|milligram[s]?|milligramme[s]?|g|gram[s]?|gramme[s]?|kg|kilogram[s]?|kilogramme[s]?|pound[s]?|lb|ounce[s]?|oz|teaspoon[s]?|tsp|tablespoon[s]?|tbs|tbsp|fluid\sounce[s]?|fl\soz|gill[s]?|cup[s]?|c|pint[s]?|pt|fl\spt|quart[s]?|qt|fl\sqt|gallon[s]?|gal|ml|milliliter[s]?|millilitre[s]?|cc|cubic\scentimeter[s]?|l|liter[s]?|litre[s]?|dl|deciliter[s]?|decilitre[s]?)\b'
                if not re.search(unitRegex, unit.group()):
                    unit = None
                    amount = amount.group().strip()
                    amountAndUnit = amount
                else:
                    amount = amount.group().strip()
                    unit = unit.group().strip()
                    amountAndUnit = amount + " " + unit
                # Finds final ingredient by removing amount and unit
                name = ingredient.replace(amountAndUnit, "").strip()
                # Checks to make sure there is no "and", "plus" or other keywords like that
                if re.search(r'^(and|plus|&)\b', name) or (name[0].isdigit()):
                    count = 1
                    while name[count].isdigit():
                        count = count + 1
                    if name[count] != "-":
                        name = name.replace("and", "")
                        name = name.replace("plus", "")
                        amount2 = re.search(amountRe, name)
                        unit2 = re.search(unitRe, name)
                        if not amount2.group() == None and not unit2.group() == None:
                            amount = [amount, amount2.group()]
                            unit = [unit, unit2.group()]
                            name = name.replace(amount2.group() + " " + unit2.group(), "").strip()
                name = name.replace("  ", " ")
                if name.startswith('.'):
                    name = name[1:].strip()
            # Adds ingredient to ingredients list
            self.addIngredient(Ingredient(name, amount, unit))
        pass
    
    def printIngredients(self,printBreakdown=False):
        print("\nYou will need the following ingredients:\n")
        for ingredient in self.ingredients.values():
            if printBreakdown:
                print(ingredient.getBreakdown())
            else:
                print(ingredient)

    def getIngredientsListAsString(self):
        '''
            Returns a string of all ingredients in the recipe
            This is used to read the ingredients aloud

            Returns:
                ingredients (str): A string of all ingredients in the recipe
        '''
        ingredients = "You will need the following ingredients:\n"
        for ingredient in self.ingredients:
            ingredients += str(self.ingredients[ingredient]) + ";\n"

        return ingredients

    def printInstructions(self):
        # print each instructions, appending the step number to the beginning
        step_num = 1
        for instruction in self.instructions:
            print(f"Step {step_num}: {instruction}")
            step_num += 1

    def printInstruction(self, step: int) -> None:
        # print the instruction at the given step
        print(f"Step {step}: {self.instructions[step-1]}")

    def getInstruction(self, step: int) -> None:
        # print the instruction at the given step
        return f"Step {step}: {self.instructions[step-1]}"

    def printRecipe(self, printBreakdownIng=False):
        self.printIngredients(printBreakdownIng)
        print()
        self.printInstructions()
        print()
        print("Yum! 😋")

    
