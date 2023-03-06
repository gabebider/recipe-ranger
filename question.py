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

    Returns:
        str: The answer to the question
    '''

    assert type(question) == str, "question must be a string"
    assert type(recipe) == Recipe, "recipe must be a Recipe object"
    assert type(current_step) == int, "current_step must be an int"
    assert current_step >= 0, "current_step must be within recipe bounds"
    assert current_step < len(recipe.steps), "current_step must be within recipe bounds"

    instruction = recipe.instructions[current_step]

    # normalize the question
    question = question.lower().strip()

   

    # check if "what is" question
    # i.e. "what is an oven"
    if "what is a" in question or 'what is an' in question:
        return google_search(question)

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
                    if ing.quantity == None:
                        return "No specific quantity defined for " + ing.name
                    elif ing.unit == None:
                        return ing.quantity
                    else:
                        if isinstance(ing.unit, list) and isinstance(ing.quantity, list):
                            return f"{ing.quantity[0]} {ing.unit[0]} and/of {ing.quantity[1]} {ing.unit[1]}"
                        else:
                            return f"{ing.quantity} {ing.unit}"
                elif is_substitution_question(question):
                    question = question.lower().strip()
                    return google_search(question)
                
    # if the ingredient is not in the recipe:
    if not found_a_match and (is_substitution_question(question) or is_amount_question(question)):
        return "I don't believe that is an ingredient in the recipe, sorry 😔"

    if is_temperature_question(question):
        for parse in instruction.parses:
            for modifier in parse.modifiers:
                if modifier[0] == "temperature":
                    return modifier[1]
        return "I'm sorry, I don't believe there is a temperature associated with this step 🙊🙊🙊"
    
    if is_time_question(question):
        for parse in instruction.parses:
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
                            return_str += f"{modifier[1]} "
                        else:
                            return_str += f"or {modifier[1]} "
                return return_str
        return "I'm sorry, I don't believe there is a duration or finish criteria associated with this step 👁️👄👁️"

    # Figure out if the question is vague, and if so, return a proper youtube or google search
    # check if vague question
    # i.e. "how do i do that?"
    #TODO: implement

    

    return youtube_search(question)
    return "I don't know the answer to that question yet."


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

    amount_keywords = ["how long","until","is it done","when","time"]

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

    question = question.replace(" ", "+")
    url = f"https://www.google.com/search?q={question}"
    return f"Great question! 😚 Here are some results that might help: {url} 🥰"



if __name__ == '__main__':
    pass