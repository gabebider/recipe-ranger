import json
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
    #  TODO: add rest of cases
    regex_list = [
    (r'\b(double|times|two)\b', "\nDoubling recipe!", doubleRecipe),
    (r'\b(divide|cut|half|halve)\b', "\nHalving recipe!", halfRecipe),
    (r'\b(make it vegetarian|to vegetarian|to veg|remove meat|make vegetarian)\b', "\nConverting to vegetarian!", toVegetarian),
    (r'\b(from vegetarian|from veg|add meat|non[- ]vegetarian)\b', "\nConverting from vegetarian!", fromVegetarian),
    (r'\b(make healthy|to healthy|better for you|better for me|make it healthy| healthier)\b', "\nConverting to healthy!", toHealthy),
    (r'\b(make unhealthy|to unhealthy|worse for you|worse for me|unhealthy|make it unhealthy|less healthy)\b', "\nConverting to unhealthy!", fromHealthy),
    (r'\b(gluten[ -]free|to gluten[ -]free)\b', "\nConverting to gluten-free!", toGlutenFree),
    (r'\b(lactose)\b', "\nConverting to lactose-free!", toLactoseFree),
    (r'\b(mexican|to mexican)\b', "\nConverting to Mexican!", toMexican),
    (r'\b(indian|to indian)\b', "\nConverting to Indian!", toIndian),
    ]

    newInstructionsList = instructionsList
    newIngList = ingredientsList

    def voiceOrPrint(text):
        if voice:
            reader(text, engine=engine)
        else:
            print(text)

    for regex, message, function in regex_list:
        if re.search(regex, input):
            voiceOrPrint(message)
            newIngList, newInstructionsList = function(ingredientsList, instructionsList, voice, engine)
            break
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

def doubleRecipe(ingList, instList, voice, engine):
    for ingKey in ingList:
        ingredient = ingList[ingKey]
        if ingredient.quantity != "":
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
    return ingList, instList

def halfRecipe(ingList, instList, voice, engine):
    for ingKey in ingList:
        ingredient = ingList[ingKey]
        if ingredient.quantity != "":
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
    return ingList, instList

def toVegetarian(ingList, instList, voice, engine):
    meatToVeg = {"beef": "beyond meat", "sausage flavored spaghetti sauce": "vegitarian spaghetti sauce", "skinless, boneless chicken breast halves": "tofu", "chicken breast": "tofu", "chicken": "tofu", "pork": "jackfruit", "fish": "tofu", "shrimp": "tofu", "turkey": "tofurky", "lamb": "seitan", "duck": "tempeh", "crab": "artichoke hearts", "bacon": "coconut bacon", "sausage": "beyond meat sausage", "pepperoni": "vegan pepperoni", "meatballs": "gardein meatless meatballs", "salmon": "smoked carrot", "oysters": "oyster mushrooms", "scallops": "king oyster mushrooms", "hamburger": "beyond meat burger", "hot dogs": "beyond meat sausage", "steak": "portobello mushroom steak", "bratwurst": "beyond meat sausage", "kielbasa": "beyond meat sausage", "crab cakes": "artichoke cake", "lobster": "artichoke hearts", "mussels": "oyster mushrooms", "quail": "tempeh", "rabbit": "seitan", "sausage rolls": "beyond meat sausage roll", "venison": "seitan", "anchovies": "tofu", "corned beef": "tempeh", "pork chops": "tempeh chops", "reuben sandwich": "tempeh sandwich", "tuna salad": "chickpea salad", "veal": "seitan", "goose": "seitan roast", "elk": "seitan steak", "horse": "soy steak", "emu": "vegan roast", "bison": "tofu steak"}
    # update ingredients
    ingList = replaceIngredient(ingList, meatToVeg, voice, engine)

    # Update instructions
    newInstructionList = replaceInstruction(instList, meatToVeg, voice, engine)
    return ingList, newInstructionList

def fromVegetarian(ingList, instList, voice, engine):
    meatToVeg = {"beef": "beyond meat", "sausage flavored spaghetti sauce": "vegitarian spaghetti sauce", "chicken breast": "tofu", "chicken": "tofu", "pork": "jackfruit", "fish": "tofu", "shrimp": "tofu", "turkey": "tofurky", "lamb": "seitan", "duck": "tempeh", "crab": "artichoke hearts", "bacon": "coconut bacon", "sausage": "beyond meat sausage", "pepperoni": "vegan pepperoni", "meatballs": "gardein meatless meatballs", "salmon": "smoked carrot", "oysters": "oyster mushrooms", "scallops": "king oyster mushrooms", "hamburger": "beyond meat burger", "hot dogs": "beyond meat sausage", "steak": "portobello mushroom steak", "bratwurst": "beyond meat sausage", "kielbasa": "beyond meat sausage", "crab cakes": "artichoke cake", "lobster": "artichoke hearts", "mussels": "oyster mushrooms", "quail": "tempeh", "rabbit": "seitan", "sausage rolls": "beyond meat sausage roll", "venison": "seitan", "anchovies": "tofu", "corned beef": "tempeh", "pork chops": "tempeh chops", "reuben sandwich": "tempeh sandwich", "tuna salad": "chickpea salad", "veal": "seitan", "goose": "seitan roast", "elk": "seitan steak", "horse": "soy steak", "emu": "vegan roast", "bison": "tofu steak", "chicken": "tofu"}
    vegToMeat = invertDict(meatToVeg)
    vegToMeat['tofu'] = 'chicken'
    # update ingredients
    ingList = replaceIngredient(ingList, vegToMeat, voice, engine)

    # Update instructions
    newInstructionList = replaceInstruction(instList, vegToMeat, voice, engine)
    return ingList, newInstructionList


def toHealthy(ingList, instList, voice, engine):
    unhealthyToHealthy = {"butter": "olive oil","sugar": "honey","white flour": "whole wheat flour","canola oil": "avocado oil","processed cheese": "feta cheese","soda": "sparkling water","white rice": "brown rice","corn syrup": "maple syrup","cream": "greek yogurt","potato chips": "kale chips","mayonnaise": "hummus","bacon": "turkey bacon","bread crumbs": "rolled oats","salt": "herbs and spices","vegetable oil": "coconut oil","white bread": "whole grain bread","canned soup": "homemade soup","canned fruits in syrup": "fresh fruits","fruit juice": "whole fruit","refined pasta": "whole grain pasta","ice cream": "frozen yogurt","chocolate chips": "cacao nibs","margarine": "avocado","beef jerky": "beef or turkey jerky with no added preservatives","energy drinks": "green tea","instant noodles": "zucchini noodles","candies": "dried fruits","sausages": "chicken sausages","whipped cream": "coconut cream","beef": "chicken","pork": "chicken","lamb": "chicken","duck": "chicken" }
    # update ingredients
    ingList = replaceIngredient(ingList, unhealthyToHealthy, voice, engine)
    
    # Update instructions
    newInstructionList = replaceInstruction(instList, unhealthyToHealthy, voice, engine)
    return ingList, newInstructionList

def fromHealthy(ingList, instList, voice, engine):
    unhealthyToHealthy = {"butter": "olive oil","sugar": "honey","white flour": "whole wheat flour","canola oil": "avocado oil","processed cheese": "feta cheese","soda": "sparkling water","white rice": "brown rice","corn syrup": "maple syrup","cream": "greek yogurt","potato chips": "kale chips","mayonnaise": "hummus","bacon": "turkey bacon","bread crumbs": "rolled oats","salt": "herbs and spices","vegetable oil": "coconut oil","white bread": "whole grain bread","canned soup": "homemade soup","canned fruits in syrup": "fresh fruits","fruit juice": "whole fruit","refined pasta": "whole grain pasta","ice cream": "frozen yogurt","chocolate chips": "cacao nibs","margarine": "avocado","beef jerky": "beef or turkey jerky with no added preservatives","energy drinks": "green tea","instant noodles": "zucchini noodles","candies": "dried fruits","sausages": "chicken sausages","whipped cream": "coconut cream","beef": "chicken","pork": "chicken","lamb": "chicken","duck": "chicken", "pork steaks": "salmon steaks"}
    healthyToUnhealthy = invertDict(unhealthyToHealthy)
    # update ingredients
    ingList = replaceIngredient(ingList, healthyToUnhealthy, voice, engine)
    
    # Update instructions
    newInstructionList = replaceInstruction(instList, healthyToUnhealthy, voice, engine)
    return ingList, newInstructionList

def toMexican(ingList, instList, voice, engine):
    # Go through all ingredients from proteinsAndSpices.json
    # See if any of the ingredients from the json are in the recipe
    # If they are, and the cuisine is not already Mexican, change it to another item of the same type from the json
    replaceDict = {}
    with open('proteinsAndSpices.json') as f:
        data = json.load(f)
        f.close()
    for ingredient in ingList:
        hasFound = False
        for item in data.keys():
            if hasFound:
                break
            if item in ingredient:
                # If the ingredient is already mexican, don't change it
                typeToReplace = data[item]['type']
                if data[item]['cuisine'] != 'mexican':
                    for foodName in data.keys():
                        if data[foodName]['type'] == typeToReplace and data[foodName]['cuisine'] == 'mexican':
                            replaceDict[item] = foodName
                            hasFound = True
                            break

    # update ingredients
    ingList = replaceSingleName(ingList, replaceDict, voice, engine)

    # Update instructions
    newInstructionList = replaceInstruction(instList, replaceDict, voice, engine)

    return ingList, newInstructionList

def toIndian(ingList, instList, voice, engine):
    replaceDict = {}
    with open('proteinsAndSpices.json') as f:
        data = json.load(f)
        f.close()
    for ingredient in ingList:
        hasFound = False
        for item in data.keys():
            if hasFound:
                break
            if item in ingredient:
                # If the ingredient is already mexican, don't change it
                typeToReplace = data[item]['type']
                if data[item]['cuisine'] != 'indian':
                    for foodName in data.keys():
                        if data[foodName]['type'] == typeToReplace and data[foodName]['cuisine'] == 'indian':
                            replaceDict[item] = foodName
                            hasFound = True
                            break

    # update ingredients
    ingList = replaceSingleName(ingList, replaceDict, voice, engine)

    # Update instructions
    newInstructionList = replaceInstruction(instList, replaceDict, voice, engine)

    return ingList, newInstructionList

def convertStyle(ingList, instList, voice, engine):
    pass

def changeCookingMethod(ingList, instList, voice, engine):
    pass

def toGlutenFree(ingList, instList, voice, engine):
    gluten_ingredients = {'wheat flour': 'almond flour','barley': 'quinoa','rye': 'oats','bread crumbs': 'gluten-free bread crumbs','pasta': 'gluten-free pasta','soy sauce': 'tamari sauce','malt vinegar': 'apple cider vinegar','beer': 'gluten-free beer','breading mix': 'gluten-free breading mix','crackers': 'gluten-free crackers','cereal': 'gluten-free cereal','pretzels': 'gluten-free pretzels','wheat germ': 'quinoa flakes','flour': 'almond flour','bread': 'gluten-free bread','croutons': 'gluten-free croutons','couscous': 'quinoa','faroe': 'quinoa','matzo': 'gluten-free matzo','muesli': 'gluten-free muesli',
                          'noodles': 'gluten-free noodles','pancake mix': 'gluten-free pancake mix','pita bread': 'gluten-free pita bread','pizza crust': 'gluten-free pizza crust','popcorn': 'gluten-free popcorn','pretzel sticks': 'gluten-free pretzel sticks','sourdough bread': 'gluten-free sourdough bread','tortillas': 'gluten-free tortillas','waffle mix': 'gluten-free waffle mix'}

    # update ingredients
    ingList = replaceIngredient(ingList, gluten_ingredients, voice, engine)

    # Update instructions
    newInstructionList = replaceInstruction(instList, gluten_ingredients, voice, engine)
    return ingList, newInstructionList

def toLactoseFree(ingList, instList, voice, engine):
    lactose_ingredients = {'milk': 'almond milk','butter': 'coconut oil','cheese': 'nutritional yeast','yogurt': 'coconut yogurt','cream': 'coconut cream','ice cream': 'coconut milk ice cream','whey protein': 'pea protein','condensed milk': 'coconut milk','evaporated milk': 'coconut milk','buttermilk': 'soy milk','cream cheese': 'vegan cream cheese','sour cream': 'coconut cream','powdered milk': 'coconut milk powder','whipped cream': 'coconut whipped cream','half and half': 'coconut milk','cottage cheese': 'tofu','ricotta cheese': 'tofu','feta cheese': 'vegan feta cheese','mascarpone cheese': 'vegan mascarpone cheese',}

    # update ingredients
    ingList = replaceIngredient(ingList, lactose_ingredients, voice, engine)

    # Update instructions
    newInstructionList = replaceInstruction(instList, lactose_ingredients, voice, engine)
    return ingList, newInstructionList

def replaceIngredient(ingredientList, substituteDict, voice, engine):
    '''
    
    :param ingredientList: list of ingredients
    :param substituteList: dict of substitutes
    '''
    # update ingredients
    for ingKey in ingredientList:
        ingredient = ingredientList[ingKey]
        done = False
        for newIngredient in substituteDict.keys():
            if done == False:
                if newIngredient in ingredient.name:
                    done = True
                    ingredient.name = ingredient.name.replace(newIngredient, substituteDict[newIngredient])
                    ingredientList[ingKey] = ingredient
                    print("Replaced " + newIngredient + " with " + substituteDict[newIngredient])
    
    return ingredientList

def replaceInstruction(instructionList, substituteDict, voice, engine):
    '''

    :param instructionList: list of instructions
    :param substituteList: dict of substitutes
    '''
    # Update instructions
    newInstructionList = []
    for instruction in instructionList:
        for ingredient in substituteDict.keys():
            if ingredient in instruction.get_text():
                newInstructionText = instruction.get_text().replace(ingredient, substituteDict[ingredient])
                instruction.set_text(newInstructionText)
        newInstructionList.append(instruction)
    return newInstructionList

def replaceSingleName(ingredientList, substituteDict, voice, engine):
    '''
    
    :param ingredientList: list of ingredients
    :param substituteList: dict of substitutes
    '''
    # update ingredients
    for ingKey in ingredientList:
        ingredient = ingredientList[ingKey]
        done = False
        for newIngredient in substituteDict.keys():
            if done == False:
                if newIngredient in ingredient.name:
                    done = True
                    ingredient.name = ingredient.name.replace(newIngredient, substituteDict[newIngredient])
                    ingredientList[ingKey] = ingredient
                    print("Replaced " + newIngredient + " with " + substituteDict[newIngredient])
    
    return ingredientList



def invertDict(d):
    return {v: k for k, v in d.items()}

