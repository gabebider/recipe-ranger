import re
from Recipe import Recipe
from Ingredient import Ingredient
from bs4 import BeautifulSoup
import requests
from voiceToTextProofOfConcept import listener, reader
import pyttsx3

# determines what type of recipe mutation the user wants to occur
def mutationType(input, ingredientsList, voice, engine):
    # Regexes to use
    doubleRecipeRegex = r'\b(double|times|two)\b'
    halfRecipeRegex = r'\b(divide|cut|half)\b'
    toVegitarianRegex = r'\b(to vegitarian|to veg|remove meat)\b'
    fromVegitarianRegex = r'\b(from vegitarian|from veg|add meat)\b'
    toHealthyRegex = r'\b(make healthy|to healthy|better for you|better for me)\b'

    # Conditional statements
    if re.search(doubleRecipeRegex, input):
        newIngList = doubleRecipe(ingredientsList, voice, engine)
    elif re.search(halfRecipeRegex, input):
        newIngList = halfRecipe(ingredientsList, voice, engine)
    elif re.search(toVegitarianRegex, input):
        newIngList = toVegitarian(ingredientsList, voice, engine)
    elif re.search(fromVegitarianRegex, input):
        newIngList = fromVegitarian(ingredientsList, voice, engine)
    elif re.search(toHealthyRegex, input):
        newIngList = toHealthy(ingredientsList, voice, engine)
    #  TODO: add rest of if cases
    return newIngList

def doubleRecipe(ingList, voice, engine):
    pass

def halfRecipe(ingList, voice, engine):
    pass

def toVegitarian(ingList, voice, engine):
    pass

def fromVegitarian(ingList, voice, engine):
    pass

def toHealthy(ingList, voice, engine):
    pass

def convertStyle(ingList, voice, engine):
    pass

def changeCookingMethod(ingList, voice, engine):
    pass

def toGlutenFree(ingList, voice, engine):
    pass

def toLactoseFree(ingList, voice, engine):
    pass