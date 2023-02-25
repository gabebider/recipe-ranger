from recipe_scrapers import scrape_me
from pprint import pprint
from Recipe import Recipe
import spacy
from RecipeFinder import RecipeFinder
import re
from navigation import isNavigation, doNavigation

class Runner():
    def __init__(self, link=None):
        # Get the recipe link
        # link = get_recipe_link()

        # 1. Get recipe either from url or from recipe search
        
        if link == None:
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
        else:
            print(f"Using provided link: {link}")
            #

        # initialize the recipe object, and get from URL or parse depending on website source
        self.recipe = Recipe(url=link)
        if re.search(r'www.allrecipes.com', link):
            self.recipe.getIngredientsFromUrl()
        else:
            self.recipe.parseForIngredients()
        
        # Scrape the recipe page using recipe_scrapers
        scraper = scrape_me(link)
        self.splitAndAddInstructions(scraper)
        
        print("Here are the ingredients you will need:")
        self.recipe.printIngredients()
        print()
        # 4. Option to see all steps or just the first step
        showAllSteps = input("Would you like to see all of the steps or just the first step?: ").lower().strip()
        print()
        regexAll = r'\b(all|all of them|all of the steps|all of the instructions|all of the directions)\b'
        regexFirst = r'\b(first|first step|first one|first instruction|first direction)\b'
        showAllStepsSelection = False
        while not showAllStepsSelection:
            if re.search(regexAll, showAllSteps):
                self.recipe.printInstructions()
                showAllStepsSelection = True
                self.step = 1
            elif re.search(regexFirst, showAllSteps):
                self.step = 1
                showAllStepsSelection = True
            else:
                showAllSteps = input("I'm sorry, I don't understand that response. Would you like to see all of the steps or just the first step?").lower().strip()

        print("\nHere is the first step:")
        # 5. For all steps
        while self.step < len(self.recipe.instructions):
        #     1. Output text
            print()
            self.recipe.printInstruction(self.step)
        #     2. Get input
            response = input("What would you like to do next?: \n").lower().strip()
        #   If input is question
            if self.isQuestion(response, self.recipe):
        #         - TODO - Make list of question words
        #         1. Determine if question is about ingredients
        #             1. What is X?
        #             2. What can I substitute for X?
        #         2. Determine if question is about steps
        #         3. Determine if question is about parameters
        #             1. What is the temperature?
        #             2. What is the time?
        #             3. How much of X?
                pass
        #   If input is navigation
            elif isNavigation(response):
        #       Do navigation
                self.step = doNavigation(response, self.step)
                
        #   If input is not question or navigation
            else:
                print("I'm sorry Larry, I don't understand that response.")

    def isQuestion(self, text: str, recipe: Recipe) -> bool:
        return False
    
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
    Runner(link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/')