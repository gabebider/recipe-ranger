from recipe_scrapers import scrape_me
from Instruction import Instruction
from Recipe import Recipe
import spacy
from RecipeFinder import RecipeFinder
import re
from utils import merge_compound_and_proper_nouns, merge_hyphenated_tokens
from navigation import isAllIngredients, isNavigation, doNavigation, isAllSteps
from question import isGeneralQuestion, questionParser
from voiceToTextProofOfConcept import listener, reader
import pyttsx3
from recipeMutations import mutationType
import datetime as dt
from pprint import pprint

class Runner():
    def __init__(self, link=None, voice=False):
        # if the user wants to use voice then initialize the text-to-speech engine
        engine = pyttsx3.init()
        # Get recipe either from url or from recipe search
        if link == None:
            link = self.getRecipeLink()
        else:
            print(f"Using provided link: {link}")

        nlp = spacy.load("en_core_web_trf")
        nlp.add_pipe("merge_hyphenated_tokens")
        nlp.add_pipe("merge_compound_and_proper_nouns")
        # initialize the recipe object, and get from URL or parse depending on website source
        self.recipe = Recipe(url=link,nlp=nlp)

        # Scrape the recipe page using recipe_scrapers
        scraper = scrape_me(link)

        if re.search(r'allrecipes.com', link):
            self.recipe.getIngredientsFromUrl()
        else:
            self.recipe.parseForIngredients(scraper=scraper)
        

        self.splitAndAddInstructions(scraper,nlp=nlp)

        # Print Ingredients
        if voice:
            reader(self.recipe.getIngredientsListAsString(), engine=engine)
        else:
            self.recipe.printIngredients(False)
        print()

        # Option to mutate the recipe
        self.recipeAltering(voice, engine)

        # Option to see all steps or just the first step
        self.allOrFirstStep(voice, engine)

        # General flow of analyzing steps or going to previous/next step
        self.interactiveSteps(voice, engine)

        # End of recipe
        if voice:
            reader("Thanks for cooking with me. That's the end of the recipe! Hope you enjoy!", engine=engine)
        else:
            print("Thanks for cooking with me. That's the end of the recipe! Hope you enjoy!")

    # Gets the recipe link from one of two methods
    def getRecipeLink(self):
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
                recipeMethod = input("I'm sorry, I don't understand that response. Would you like to search for a recipe or provide your own link to one? ").lower().strip()
        return link
    
    # Determines whether or not to show all steps
    def allOrFirstStep(self, voice, engine):
        # asks for preference
        if voice:
            reader("Would you like to see all of the steps or just the first step?", engine=engine)
            showAllSteps, confidence = listener()
            showAllSteps = showAllSteps.lower().strip()
        else:
            showAllSteps = input("Would you like to see all of the steps or just the first step?: ").lower().strip()
        print()

        # Uses regex to determine response
        regexAll = r'\b(all|all of them|all of the steps|all of the instructions|all of the directions)\b'
        regexFirst = r'\b(first|first step|first one|first instruction|first direction)\b'
        showAllStepsSelection = False
        while not showAllStepsSelection:
            if re.search(regexAll, showAllSteps):
                self.recipe.printInstructions()
                showAllStepsSelection = True
                self.step = 0
            elif re.search(regexFirst, showAllSteps):
                self.step = 1
                showAllStepsSelection = True
            else:
                # Asks again if regex can't determine
                if voice:
                    reader("I'm sorry, I don't understand. Would you like to see all of the steps or just the first step?", engine=engine)
                    showAllSteps, confidence = listener()
                    showAllSteps = showAllSteps.lower().strip()
                else:
                    showAllSteps = input("I'm sorry, I don't understand that response. Would you like to see all of the steps or just the first step?" ).lower().strip()

    # All interaction with user after initial selections happens here
    def interactiveSteps(self, voice, engine):
        if(self.step == 1):
            if voice:
                reader("There are " + str(len(self.recipe.instructions)) + " steps in this recipe.", engine=engine)
                reader("\nHere is the first step:", engine=engine)
            else:
                print("There are " + str(len(self.recipe.instructions)) + " steps in this recipe.")
                print("\nHere is the first step:")
        # 5. For all steps
        currStep = -1
        while self.step < len(self.recipe.instructions) + 1:
        #     1. Output text
            print()
            if (voice and self.step > 0) and currStep != self.step:
                reader(self.recipe.getInstruction(self.step), engine=engine)
                print()
            elif self.step > 0 and currStep != self.step:
                self.recipe.printInstruction(self.step)
                print()
        #     2. Get input
            currStep = self.step
            if voice:
                reader("What would you like to do next?: \n")
                response, confidence = listener()
                response = response.lower().strip()
            else:
                response = input("What would you like to do next?: \n").lower().strip()
        #   If input is question
            if isGeneralQuestion(response):
                if voice:
                    reader(questionParser(response, self.recipe, currStep), engine=engine)
                else:
                    print(questionParser(response, self.recipe, currStep))
        #   If input is navigation
            elif isNavigation(response):
                if isAllSteps(response):
                    print()
                    self.recipe.printInstructions()
                elif isAllIngredients(response):
                    print()
                    self.recipe.printIngredients(False)
                else:
                    # Do navigation
                    currStep = -1
                    tempStep = doNavigation(response, self.step)
                    # Checks if step is out of bounds
                    if tempStep < 1:
                        if voice:
                            reader("\nStep out of bounds. Showing Step 1.", engine=engine)
                        else:
                            print("\nStep out of bounds. Showing Step 1.")
                        self.step = 1
                    elif tempStep > len(self.recipe.instructions) + 1:
                        if voice:
                            reader("\nStep out of bounds. Showing final step instead.", engine=engine)
                        else:
                            print("\nStep out of bounds. Showing final step instead.")
                        self.step = len(self.recipe.instructions)
                    else:
                        self.step = tempStep
                    
        #   If input is not question or navigation
            else:
                if voice:
                    reader("I'm sorry Larry, I don't understand that response.", engine=engine)
                else:
                    print("I'm sorry Larry, I don't understand that response.")

    # Determines if there will be a recipe mutation, and if there is, it calls the mutationType file
    def recipeAltering(self, voice, engine):
        if voice:
            reader("Would you like to alter the recipe?", engine=engine)
            mutateRecipe, confidence = listener()
        else:
            mutateRecipe = input("Would you like to alter the recipe? ")
        
        # Chekcs if the user wants to edit the recipe
        mutateRecipeRegex = r'\b(yes|yeah|sure|ok(?:ay)?|transform|mutate|change)\b'
        if re.search(mutateRecipeRegex, mutateRecipe.lower().strip()):
            if voice:
                reader("\nGreat! How would you like to alter the recipe?", engine=engine)
                mutation, confidence = listener()
            else:
                mutation = input("\nGreat! How would you like to alter the recipe? ")
            self.recipe.replaceIngredientsList(mutationType(mutation.lower().strip(), self.recipe.getIngredientsList(), voice, engine))
        
        # read new recipe
        if voice:
            reader("\nYour updated ingredients list is:\n", engine=engine)
            reader(self.recipe.getIngredientsListAsString(), engine=engine)
        else:
            print("\nYour updated ingredients list is:\n")
            self.recipe.printIngredients(False)
        pass

    # Splits and adds instructions
    def splitAndAddInstructions(self, scraper, nlp):
        instructions = scraper.instructions()
        instructions = instructions.replace("\n", "")
        instructions = re.sub(r"(?<![0-9])\.(?![0-9])",". ",instructions)
        instructions = instructions.replace("; ", ". ")

        instructions = instructions.split(". ")

        instructions = [instruction.strip() + "." for instruction in instructions if instruction.strip() != ""]

        for instruction in instructions:
            self.recipe.addInstruction(Instruction(instruction,nlp))

if __name__ == '__main__':
    Runner(voice=False)