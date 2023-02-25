import requests
from bs4 import BeautifulSoup
from Ingredient import Ingredient
from recipe_scrapers import scrape_me

class Recipe():
    def __init__(self, url, ingredients = {}, instructions = []):
        self.url = url
        self.ingredients = ingredients
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
        pass
    
    def printIngredients(self,printBreakdown=False):
        print()
        print("You will need the following ingredients:")
        print()
        for ingredient in self.ingredients.values():
            if printBreakdown:
                print(ingredient.getBreakdown())
            else:
                print(ingredient)

    def printInstructions(self):
        # print each instructions, appending the step number to the beginning
        step_num = 1
        for instruction in self.instructions:
            print(f"Step {step_num}: {instruction}")
            step_num += 1

    def printRecipe(self):
        self.printIngredients()
        print()
        self.printInstructions()
        print()
        print("Yum! 😋")

    
