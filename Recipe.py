import requests
from bs4 import BeautifulSoup
from Ingredient import Ingredient
from collections import defaultdict
from recipe_scrapers import scrape_me
import re
from utils import get_obj_text, get_conjuncts, parseIngredientCore
import spacy
from Instruction import Instruction

class Recipe():
    def __init__(self, url: str, nlp: spacy.language.Language):
        assert isinstance(url, str), "url must be a string"
        assert isinstance(nlp, spacy.language.Language), "nlp must be a spacy language object"

        self.url = url
        self.ingredients = {}
        self.instructions = []
        self.nlp = nlp

    def replaceIngredientsListAndInstructionsList(self, ingredientAndStepList):
        assert isinstance(ingredientAndStepList, list), "ingredientAndStepList must be a list"
        assert len(ingredientAndStepList) == 2, "ingredientAndStepList must be a list of length 2"
        self.ingredients = ingredientAndStepList[0]
        self.instructions = ingredientAndStepList[1]

    def getIngredientsList(self):
        return self.ingredients
    
    def getInstructionsList(self):
        return self.instructions
    
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
            newIngredient = Ingredient("", "", "", self.nlp)
            for section in sections:
                if 'data-ingredient-quantity' in section.attrs:
                    newIngredient.setQuantity(section.text.strip())
                elif 'data-ingredient-unit' in section.attrs:
                    newIngredient.setUnit(section.text.strip())
                elif 'data-ingredient-name' in section.attrs:
                    newIngredient.setName(section.text.strip())

            self.addIngredient(newIngredient)
    
    def parseForIngredients(self,scraper):
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
            self.addIngredient(Ingredient(name, amount, unit, self.nlp))
        
    
    def printIngredients(self,printBreakdown=False):
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
            tempInstruction  = instruction.text[0].upper() + instruction.text[1:]
            print(f"Step {step_num}: {tempInstruction}")
            step_num += 1

    def getInstructionToolsAsString(self, step: int) -> str:
        assert isinstance(step, int), "step must be an integer"
        if step < 1:
            step == 1
        elif step > len(self.instructions):
            step == len(self.instructions)

        instruction = self.instructions[step-1]
        tools = instruction.tools

        if len(tools) == 0:
            return "\nNo tools are explicitly mentioned in this step\n"
        
        else:
            toolsString = "\nThe tools explicitly mentioned in this step are:\n"
            for tool in tools:
                toolsString += f"  - {tool}\n"
            return toolsString


    def getInstructionsAsString(self):
        '''
            Returns a string of all instructions in the recipe
            This is used to read the instructions aloud

            Returns:
                instructions (str): A string of all instructions in the recipe
        '''
        instructions = "Instructions:\n"
        step_num = 1
        for instruction in self.instructions:
            tempInstruction = instruction.text[0].upper() + instruction.text[1:]
            # print(f"Step {step_num}: {tempInstruction}")
            instructions += f"Step {step_num}: {tempInstruction};\n"
            step_num += 1

        return instructions

    def printInstruction(self, step: int) -> None:
        # print the instruction at the given step
        # capitalize the first letter of the instruction
        instruction = self.instructions[step-1]
        tempInstruction = instruction.text[0].upper() + instruction.text[1:]
        print(f"Step {step}: {tempInstruction}")

    def getInstruction(self, step: int) -> None:
        # print the instruction at the given step
        instruction = self.instructions[step-1]
        tempInstruction = instruction.text[0].upper() + instruction.text[1:]
        return f"Step {step}: {tempInstruction}"

    def printRecipe(self, printBreakdownIng=False):
        self.printIngredients(printBreakdownIng)
        print()
        self.printInstructions()
        print()
        print("Yum! 😋")

    def getToolsAsString(self):
        s = "\nThe recipe explicity mentions the following tools, however you may need to use other tools for certain steps at your own discretion:\n\n"
        for tool in self.tools:
            s += f"  - {tool}\n"
        return s
        
    def getInstructionObject(self, step: int) -> Instruction:
        # return the instruction at the given step
        return self.instructions[step-1]

    def identify_tools(self):

        # fill a set with tools from `tools.txt`
        tools = set()
        with open('tools.txt','r') as f:
            for line in f:
                tools.add(line.strip())
        
        def in_tools(token):
            core = parseIngredientCore(token.text,self.nlp)
            core = core['core']
            return core in tools
        
        def merge_substring_keys(dictionary):
            keys = list(dictionary.keys())
            for i, key1 in enumerate(keys):
                for key2 in keys[i+1:]:
                    if key1 in key2:
                        dictionary[key2] |= dictionary[key1]
                        del dictionary[key1]
                        break
            return dictionary

        objs = set()
        for idx, instruction in enumerate(self.instructions):
            doc = self.nlp(instruction.text)
            for token in doc:
                if token.dep_ in ["dobj","pobj"]:
                    objs.add((token,idx))

        # get any objects that are connected to another object by a cc
        objs = get_conjuncts(objs)

        # filter out objects that are not tools
        objs = {obj for obj in objs if in_tools(obj[0])}

        # create dict mapping tools to instructions where they are used
        tools_used_dict = defaultdict(set)
        for obj in objs:
            tools_used_dict[get_obj_text(obj[0])].add(obj[1])

        # sort in increasing order of length of key
        tools_used_dict = dict(sorted(tools_used_dict.items(), key=lambda item: len(item[0].split())))
        # merge keys that are substrings of other keys
        tools_used_dict = merge_substring_keys(tools_used_dict)

        self.tools = list(tools_used_dict.keys())

        for tool in self.tools:
            for instruction in tools_used_dict[tool]:
                self.instructions[instruction].add_tool(tool)



            
    
