from recipe_scrapers import scrape_me
from pprint import pprint
from Recipe import Recipe
import spacy
from RecipeFinder import RecipeFinder
import re
from navigation import isNavigation, doNavigation
from question import isGeneralQuestion, questionParser
from voiceToTextProofOfConcept import listener, reader
import pyttsx3

class Runner():
    def __init__(self, link=None, voice=False):
        # if the user wants to use voice then initialize the text-to-speech engine
        engine = pyttsx3.init()
        # Get recipe either from url or from recipe search
        if link == None:
            link = self.getRecipeLink()
        else:
            print(f"Using provided link: {link}")

        # initialize the recipe object, and get from URL or parse depending on website source
        self.recipe = Recipe(url=link)
        if re.search(r'allrecipes.com', link):
            self.recipe.getIngredientsFromUrl()
        else:
            self.recipe.parseForIngredients()
        
        # Scrape the recipe page using recipe_scrapers
        scraper = scrape_me(link)
        self.splitAndAddInstructions(scraper)

        # Print Ingredients
        if voice:
            reader(self.recipe.getIngredientsListAsString(), engine=engine)
        else:
            self.recipe.printIngredients(False)
        print()

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
                recipeMethod = input("I'm sorry, I don't understand that response. Would you like to search for a recipe or provide your own link to one?").lower().strip()
        return link
    
    def allOrFirstStep(self, voice, engine):
        if voice:
            reader("Would you like to see all of the steps or just the first step?", engine=engine)
            showAllSteps, confidence = listener()
            showAllSteps = showAllSteps.lower().strip()
        else:
            showAllSteps = input("Would you like to see all of the steps or just the first step?: ").lower().strip()
        print()
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
                if voice:
                    reader("Would you like to see all of the steps or just the first step?", engine=engine)
                    showAllSteps, confidence = listener()
                    showAllSteps = showAllSteps.lower().strip()
                else:
                    showAllSteps = input("I'm sorry, I don't understand that response. Would you like to see all of the steps or just the first step?").lower().strip()

    # All interaction with user after initial selections happens here
    def interactiveSteps(self, voice, engine):
        if(self.step == 1):
            if voice:
                reader("\nHere is the first step:", engine=engine)
            else:
                print("\nHere is the first step:")
        # 5. For all steps
        currStep = -1
        while self.step < len(self.recipe.instructions):
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
        #         - TODO - Make list of question words
        #         1. Determine if question is about ingredients
        #             1. What is X?
        #             2. What can I substitute for X?
        #         2. Determine if question is about steps
        #         3. Determine if question is about parameters
        #             1. What is the temperature?
        #             2. What is the time?
        #             3. How much of X?
                if voice:
                    reader(questionParser(response, self.recipe), engine=engine)
                else:
                    print(questionParser(response, self.recipe))
        #   If input is navigation
            elif isNavigation(response):
        #       Do navigation
                currStep = -1
                self.step = doNavigation(response, self.step)
                
        #   If input is not question or navigation
            else:
                if voice:
                    reader("I'm sorry Larry, I don't understand that response.", engine=engine)
                else:
                    print("I'm sorry Larry, I don't understand that response.")

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
    Runner(voice=False)