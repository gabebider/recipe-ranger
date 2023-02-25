from recipe_scrapers import scrape_me
from pprint import pprint
from Recipe import Recipe
import spacy
from RecipeFinder import RecipeFinder
import re

class Runner():
    def __init__(self):
        # Get the recipe link
        # link = get_recipe_link()

        # Chose recipe method
        recipeMethod = input("Would you like to search for a recipe or provide your own link to one?: ").lower().strip()
        regexSearch = r'\b(search|look( up)?|google|find|first|former)\b'
        regexProvide = r'\b(link|provide|second|own|latter)\b'
        methodSelection = False
        while not methodSelection:
            if re.search(regexSearch, recipeMethod):
                link = RecipeFinder()
                methodSelection = True
            elif re.search(regexProvide, recipeMethod):
                link = input("Please provide the link to the recipe: ").strip()
                methodSelection = True
            else:
                recipeMethod = input("I'm sorry, I don't understand that response. Would you like to search for a recipe or provide your own link to one?").lower().strip()
                
        #link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

        # initialize the recipe object
        self.recipe = Recipe(url=link)
        self.recipe.getIngredientsFromUrl()
        # Scrape the recipe page using recipe_scrapers
        scraper = scrape_me(link)
        self.splitAndAddInstructions(scraper)

        self.recipe.printRecipe()



        # Display step 1 and ask user for input

        # Check if verb is information or navigation

        # If ingredient, then use parser to find ingredient

        # If navigation, then navigate in indicated direction

    def splitAndAddInstructions(self, scraper):
        instructions = scraper.instructions()
        instructions = instructions.replace("\n", "")
        instructions = re.sub(r"(?<![0-9])\.(?![0-9])",". ",instructions)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(instructions)
        for sent in doc.sents:
            assert sent != None, "Sentence is None"
            self.recipe.addInstruction(sent)

if __name__ == '__main__':
    Runner()