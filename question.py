import re
from Recipe import Recipe
from Ingredient import Ingredient
from bs4 import BeautifulSoup
import requests

# TODO: @Gabe - write code to handle questions such as "substitute", "what is X", "what can I use instead of X", etc.
# these can be found in flow.md
# for time being, just return a google search

def tokenize(text: str) -> list:
	""" 
	Given a string, return a list of the lowercase tokens (words) in that string

    Parameters:
        text (str): The string to be tokenized

    Returns:    
        list: A list of the lowercase tokens (words) in the string
	"""
	# Split this text on any whitespace, then for each section
	# * remove any non alphabetic character ([^A-Za-z])
	# * convert to lowercase
	# * strip away any extra whitespace
	tokens = [re.sub(r'[^A-Za-z]+', '', s).lower().strip() for s in  text.split()]
	return tokens


def isGeneralQuestion(sentence: str) -> bool:
    '''
        This function takes a sentence and returns True if it is a question, False otherwise.

        Parameters:
            sentence (str): The sentence to be checked

        Returns:    
            bool: True if the sentence is a question, False otherwise
    '''

    assert type(sentence) == str, "sentence must be a string"

    # normalize the sentence
    sentence = sentence.lower().strip()
    if sentence.endswith('?'):
        return True

    # tokenize the sentence
    sentence_tokens = tokenize(sentence)
    # NOTE: this does not include the word `can` as a question word
    # because the word `can` is used for navigational purposes
    # but we may want to revisit this
    question_words = {"what", "when", "where", "which", "who", "whom", "whose", "why", "how"}
    for token in sentence_tokens:
        if token in question_words:
            return True
    
    return False
        
def questionParser(question: str, recipe: Recipe, current_step: int) -> str:
    '''
    This function takes a question and returns a string with the answer.

    Parameters:
        question (str): The question to be parsed
        recipe (Recipe): The recipe to be used to answer the question
        current_step (int): The current step of the recipe

    Returns:
        str: The answer to the question
    '''

    assert type(question) == str, "question must be a string"
    assert type(recipe) == Recipe, "recipe must be a Recipe object"
    assert type(current_step) == int, "current_step must be an int"
    assert current_step >= 0, "current_step must be within recipe bounds"
    assert current_step <= len(recipe.instructions), "current_step must be within recipe bounds"

    instruction = recipe.instructions[current_step-1]

    # normalize the question
    question = question.lower().strip()

    # check if question is about the ingredients
    # i.e. "how much flour do I need?"
    # i.e. "what can i replace the flour with?"
    # i.e. "what can i substitute for the flour?"
    question_tokens = tokenize(question)
    # create list of noramlized ingredients
    ingredient_names = [ingredient for ingredient in recipe.ingredients]

    found_a_match = False
    for token in question_tokens:
        for ingredient_name in ingredient_names:
            if re.search(r'\b{}\b'.format(token), ingredient_name.lower().strip()):
                found_a_match = True
            # question is asking about ingredient: `token`
            # determine is the question is asking about the amount
                if is_amount_question(question):
                    ing = recipe.ingredients[ingredient_name]
                    if ing.quantity == "":
                        return "No specific quantity defined for " + ing.name
                    elif ing.unit == "":
                        return ing.quantity + "are needed for the whole recipe."
                    else:
                        if isinstance(ing.unit, list) and isinstance(ing.quantity, list):
                            return f"{ing.quantity[0].strip()} {ing.unit[0].strip()} and/of {ing.quantity[1].strip()} {ing.unit[1].strip()} are needed for the whole recipe."
                        else:
                            return f"{ing.quantity.strip()} {ing.unit.strip()} are needed for the whole recipe."
                elif is_substitution_question(question):
                    question = question.lower().strip()
                    return google_search(question)
                
    # if the ingredient is not in the recipe:
    if not found_a_match and (is_substitution_question(question) or is_amount_question(question)):
        return "I don't believe that is an ingredient in the recipe, sorry 😔"

    if is_temperature_question(question):
        for parse in instruction.parses.values():
            for modifier in parse.modifiers:
                if modifier[0] == "temperature":
                    return modifier[1]
        return "I'm sorry, I don't believe there is a temperature associated with this step 🙊🙊🙊"
    
    if is_time_question(question):
        for parse in instruction.parses.values():
            relevant_modifiers = []

            for modifier in parse.modifiers:
                if modifier[0] == "time":
                    relevant_modifiers.append(modifier)
            
            for modifier in parse.modifiers:
                if modifier[0] == "until":
                    relevant_modifiers.append(modifier)

            if len(relevant_modifiers) > 0:
                return_str = ""
                for ind, modifier in enumerate(relevant_modifiers):
                    if modifier[0] == "time":
                        return_str += f"for {modifier[1]} "
                    elif modifier[0] == "until":
                        if ind == 0:
                            if "until" not in modifier[1]:
                                return_str += f"until {modifier[1]} "
                            else:
                                return_str += f"{modifier[1]} "
                        else:
                            if "until" not in modifier[1]:
                                return_str += f"or until {modifier[1]} "
                            else:
                                return_str += f"or {modifier[1]} "
                return return_str
        return "I'm sorry, I don't believe there is a duration or finish criteria associated with this step 👁️👄👁️"

    if is_all_tools_question(question):
        return recipe.getToolsAsString()
    elif is_tool_question(question):
        return recipe.getInstructionToolsAsString(current_step)
    # Figure out if the question is vague, and if so, return a proper youtube or google search
    # check if vague question
    if is_all_instruction_question(question):
        return recipe.getInstructionsAsString()

    
    if is_all_ingredient_question(question):
        return recipe.getIngredientsListAsString()
    
    if is_vague_question(question):
        currentInstruction = recipe.getInstructionObject(current_step)
        # if is_action_or_information_question(question) == "action":
        #     return youtube_search(currentInstruction.text)
        # elif is_action_or_information_question(question) == "information":
        #     return google_search(currentInstruction.text)
        return google_search(currentInstruction.text)

    return "I don't know the answer to that question yet."

def is_all_instruction_question(question: str) -> bool:
    if ("all" in question or "the" in question) and ("instructions" in question or "steps" in question):
        return True
    
def is_all_ingredient_question(question: str) -> bool:
    if ("all" in question or "the" in question) and ("ingredients" in question or "items" in question):
        return True
    
def is_amount_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a question about an ingredient's amount, False otherwise.

    Parameters:
        question (str): The question to be checked

    Returns:
        bool: True if the question is about an ingredient's amount, False otherwise
     '''

    assert type(question) == str, "question must be a string"

    # normalize the question
    question = question.lower().strip()

    amount_keywords = ["amount", "how much", "how many"]
    for keyword in amount_keywords:
        if keyword in question:
            return True
    
    return False

def is_tool_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a tool question, False otherwise.
    '''

    assert type(question) == str, "question must be a string"

    # normalize the question
    question = question.lower().strip()
    question = re.sub(r"[^a-zA-Z\s]+", "", question)

    tool_keywords = ["tool", "tools", "utensil", "utensils", "equipment"]
    for keyword in tool_keywords:
        if keyword in question:
            return True
    return False

def is_all_tools_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a tool question, specifically asking about all tools, False otherwise.
    '''
    assert type(question) == str, "question must be a string"

    question = question.lower().strip()
    question = re.sub(r"[^a-zA-Z\s]+", "", question)

    if not is_tool_question(question):
        return False
    
    all_keywords = ["all","every","each","whole"]
    for keyword in all_keywords:
        if keyword in question:
            return True
    return False

def is_vague_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a vague question, False otherwise.

    Parameters:
        question (str): The question to be checked

    Returns:
        bool: True if the question is vague, False otherwise
    '''

    assert type(question) == str, "question must be a string"

    # normalize the question
    question = question.lower().strip()
    question = re.sub(r"[^a-zA-Z\s]+", "", question)


    vague_keywords = ["how do i do that", "what is this", "how", "what" , "whats that", "why"]
    
    for keyword in vague_keywords:
        if keyword == question:
            # print("vague question")
            return True
    
    return False

def is_action_or_information_question(question: str) -> str:
    '''
    This function takes a question and returns "action" if it is a question about an action, "information" if it is a question about information, and "unknown" if it is neither.

    Parameters:
        question (str): The question to be checked

    Returns:
        str: "action" if the question is about an action, "information" if the question is about information, and "unknown" if it is neither
    '''

    assert type(question) == str, "question must be a string"


    # normalize the question
    question = question.lower().strip()

    action_keywords = ["how do", "how do i", "how do i do", "how do i do that", "how do i do that?", "how do i do that?"]
    information_keywords = ["what is", "what is a", "what is an", "what is the", "what is the difference", "what is the difference between", "what is the difference between a", "what is the difference between an", "what is the difference between the", "what is the difference between the two", "what is the difference between the two?", "what is the difference between the two?"]
    for keyword in action_keywords:
        if keyword in question:
            # print("action question")
            return "action"
    for keyword in information_keywords:
        if keyword in question:
            # print("information question")
            return "information"
    return "unknown"

def is_substitution_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a question about substituting an ingredient, False otherwise.

    Parameters:
        question (str): The question to be checked

    Returns:
        bool: True if the question is about substituting an ingredient, False otherwise
    '''

    assert type(question) == str, "question must be a string"
    
    # normalize the question
    question = question.lower().strip()

    substitution_words = {"substitute", "instead of", "instead", "substitution", "replace", "sub", "use", "exchange"}

    # tokenize the question
    question_tokens = tokenize(question)

    for token in question_tokens:
        if token in substitution_words:
            return True

    return False

def is_temperature_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a question about temperature, False otherwise.

    Parameters:
        question (str): The question to be checked

    Returns:
        bool: True if the question is about temperature, False otherwise
    '''

    assert type(question) == str, "question must be a string"

    # normalize the question
    question = question.lower().strip()

    temperature_words = {"temperature","heat","hot","cold","warm"}

    # tokenize the question
    question_tokens = tokenize(question)

    for token in question_tokens:
        if token in temperature_words:
            return True

    return False

def is_time_question(question: str) -> bool:
    '''
    This function takes a question and returns True if it is a question about time, False otherwise.

    Parameters:
        question (str): The question to be checked

    Returns:
        bool: True if the question is about time, False otherwise
    '''

    assert type(question) == str, "question must be a string"

    # normalize the question
    question = question.lower().strip()

    amount_keywords = ["how long","until","is it done","when","time","done"]

    for keyword in amount_keywords:
        if keyword in question:
            return True
    
    return False

def youtube_search(question: str) -> str:
    '''
    This function takes a question and returns a response with a link to a youtube video
    answering the question

    Parameters:
        question (str): The question to search

    Returns:
        str: The answer containing a link to youtube
    '''

    assert type(question) == str, "question must be a string"

    # normalize the question
    question = question.lower().strip()

    # replace spaces with +'s
    question = re.sub(r"[^a-zA-Z\s]+", "", question)
    question = question.replace(" ", "+")

    # create the url
    url = f"https://www.youtube.com/results?search_query={question}"

    return f"Great question! 😚 Here are some videos that might help: {url} 🥰"

def google_search(question: str) -> str:
    '''
    This function takes a question and returns a response with a link to a google search

    Parameters:
        question (str): The question to search  

    Returns:    
        str: The answer containing a link to google
    '''
    question = re.sub(r"[^a-zA-Z\s]+", "", question)
    question = question.replace(" ", "+")
    

    url = f"https://www.google.com/search?q={question}"
    return f"Great question! 😚 Here are some results that might help: {url} 🥰"



if __name__ == '__main__':
    pass