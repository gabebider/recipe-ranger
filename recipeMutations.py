import re
from Recipe import Recipe
from Ingredient import Ingredient
from bs4 import BeautifulSoup
import requests
from voiceToTextProofOfConcept import listener, reader
import pyttsx3
import unicodedata
import Instruction

# determines what type of recipe mutation the user wants to occur
def mutationType(input, ingredientsList, instructionsList, voice, engine):
    # Regexes to use
    doubleRecipeRegex = r'\b(double|times|two)\b'
    halfRecipeRegex = r'\b(divide|cut|half)\b'
    toVegitarianRegex = r'\b(to vegitarian|to veg|remove meat)\b'
    fromVegitarianRegex = r'\b(from vegitarian|from veg|add meat)\b'
    toHealthyRegex = r'\b(make healthy|to healthy|better for you|better for me)\b'

    # in case instructions list isnt changed
    newInstructionsList = instructionsList
    # Conditional statements
    if re.search(doubleRecipeRegex, input):
        if voice:
            reader("\nDoubling recipe!", engine=engine)
        else:
            print("\nDoubling Recipe!")
        newIngList = doubleRecipe(ingredientsList)
    elif re.search(halfRecipeRegex, input):
        if voice:
            reader("\nHalving recipe!", engine=engine)
        else:
            print("\nHalving Recipe!")
        newIngList = halfRecipe(ingredientsList)
    elif re.search(toVegitarianRegex, input):
        if voice:
            reader("\nMaking recipe vegitarian!", engine=engine)
        else:
            print("\nMaking recipe vegitarian!")
        newIngList, newInstructionsList = toVegitarian(ingredientsList, instructionsList)
    elif re.search(fromVegitarianRegex, input):
        newIngList = fromVegitarian(ingredientsList, voice, engine)
    elif re.search(toHealthyRegex, input):
        newIngList = toHealthy(ingredientsList, voice, engine)
    #  TODO: add rest of if cases
    return [newIngList, newInstructionsList]

def convertToFloat(numberString):
    splitNums = numberString.split()
    fixedNums = []
    hasFraction = False
    for num in splitNums:
        if "/" in num:
            hasFraction = True
            numerator, denominator = num.split("/")
            numerator = float(numerator)
            denominator = float(denominator)
            decimal = numerator / denominator
            fixedNums.append(decimal)
        elif len(num) == 1 and ord(num) > 127:
            hasFraction = True
            fixedNums.append(unicodedata.numeric(num))
        else:
            fixedNums.append(float(num))
    if hasFraction:
        summation = 0
        for num in fixedNums:
            summation = summation + num
        fixedNums = summation
    elif len(fixedNums) == 1:
        fixedNums = fixedNums[0]
    return fixedNums

def doubleRecipe(ingList):
    for ingKey in ingList:
        ingredient = ingList[ingKey]
        if ingredient.quantity != None:
            if isinstance(ingredient.quantity, list):
                newAmount = []
                for ing in ingredient.quantity:
                    newAmount.append(convertToFloat(ing) * 2)
            else:
                newAmount = convertToFloat(ingredient.quantity)
                if isinstance(newAmount, list):
                    newAmount[0] = newAmount[0] * 2
                    newAmount = str(newAmount[0]) + " " + str(newAmount[1])
                else:
                    newAmount = str(newAmount * 2)
        ingredient.quantity = newAmount
        ingList[ingKey] = ingredient
    return ingList

def halfRecipe(ingList):
    for ingKey in ingList:
        ingredient = ingList[ingKey]
        if ingredient.quantity != None:
            if isinstance(ingredient.quantity, list):
                newAmount = []
                for ing in ingredient.quantity:
                    newAmount.append(convertToFloat(ing) * 0.5)
            else:
                newAmount = convertToFloat(ingredient.quantity)
                if isinstance(newAmount, list):
                    newAmount[0] = newAmount[0] * 0.5
                    newAmount = str(newAmount[0]) + " " + str(newAmount[1])
                else:
                    newAmount = str(newAmount * 0.5)
        ingredient.quantity = newAmount
        ingList[ingKey] = ingredient
    return ingList

def toVegitarian(ingList, instList):
    meatToVeg = {"beef": "beyond meat", "sausage flavored spaghetti sauce": "vegitarian spaghetti sauce", "chicken breast": "tofu", "chicken": "tofu", "pork": "jackfruit", "fish": "tofu", "shrimp": "tofu", "turkey": "tofurky", "lamb": "seitan", "duck": "tempeh", "crab": "artichoke hearts", "bacon": "coconut bacon", "sausage": "beyond meat sausage", "pepperoni": "vegan pepperoni", "meatballs": "gardein meatless meatballs", "salmon": "smoked carrot", "oysters": "oyster mushrooms", "scallops": "king oyster mushrooms", "hamburger": "beyond meat burger", "hot dogs": "beyond meat sausage", "steak": "portobello mushroom steak", "bratwurst": "beyond meat sausage", "kielbasa": "beyond meat sausage", "crab cakes": "artichoke cake", "lobster": "artichoke hearts", "mussels": "oyster mushrooms", "quail": "tempeh", "rabbit": "seitan", "sausage rolls": "beyond meat sausage roll", "venison": "seitan", "anchovies": "tofu", "corned beef": "tempeh", "pork chops": "tempeh chops", "reuben sandwich": "tempeh sandwich", "tuna salad": "chickpea salad", "veal": "seitan", "goose": "seitan roast", "elk": "seitan steak", "horse": "soy steak", "emu": "vegan roast", "bison": "tofu steak"}
    # update ingredients
    for ingKey in ingList:
        ingredient = ingList[ingKey]
        done = False
        for meat in meatToVeg.keys():
            if done == False:
                if meat in ingredient.name:
                    done = True
                    ingredient.name = ingredient.name.replace(meat, meatToVeg[meat])
                    ingList[ingKey] = ingredient
    
    # Update instructions
    newInstructionList = []
    for instruction in instList:
        for meat in meatToVeg.keys():
            if meat in instruction.get_text():
                newInstText = instruction.get_text().replace(meat, meatToVeg[meat])
                instruction.set_text(newInstText)
        newInstructionList.append(instruction)
    return ingList, newInstructionList

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