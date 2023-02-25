import re
from Recipe import Recipe
from Ingredient import Ingredient
from bs4 import BeautifulSoup
import requests

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


def isQuestion(sentence: str) -> bool:
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
    question_words = set("what", "when", "where", "which", "who", "whom", "whose", "why", "how")
    for token in sentence_tokens:
        if token in question_words:
            return True
    
    return False
        
def questionParser(question: str, recipe: Recipe):
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

    # normalize the question
    question = question.lower().strip()

    # check if question is about the ingredients
    question_tokens = question.split()
    # create list of noramlized ingredients
    ingredient_names = [ingredient.lower().strip() for ingredient in recipe.ingredients]
    for token in question_tokens:
        for ingredient_name in ingredient_names:
            if token in ingredient_name:
            # question is asking about ingredient: `token`
            # determine is the question is asking about the amount
                if is_amount_question(question):
                    # if we get a KeyError, then its probably because I normalized the ingredient name
                    return str(recipe.ingredients[ingredient_name])
                else:
                    # question is not about the amount
                    return scrape_youtube_for_question(question)
    
    return scrape_youtube_for_question(question)
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

def scrape_youtube_for_question(question: str) -> str:
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
    # remove any punctuation
    question = re.sub(r'[^\w\s]', '', question)

    # create the url
    url = f"https://www.youtube.com/results?search_query={question}"

    request = requests.get(url)
    with open ("test.html", "w") as f:
        f.write(str(request.text))

    soup = BeautifulSoup(request.text, "html.parser")

    # parking lot
    # .find('div', {'id': 'contents'}).find('a')['href']

    # get the first video
    # link = soup.find('div', {'class': 'style-scope ytd-item-section-renderer'}).find('a', {'class': 'yt-simple-endpoint inline-block style-scope ytd-thumbnail'})
    a_tags = soup.find_all('a')

    for a in a_tags:
        if a.get('href'):
            return a.get('href')

    # goods = []
    # for li in link:
    #     print(li.get('href'))

    # print(goods)
    return "scraping youtube lowkey hard"
    return link



if __name__ == '__main__':
    print(scrape_youtube_for_question("how do i chop an onion"))