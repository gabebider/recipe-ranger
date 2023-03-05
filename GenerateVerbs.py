import requests
from bs4 import BeautifulSoup
import spacy
from recipe_scrapers import scrape_me
import re
from collections import defaultdict
import csv

def generateUrls(queries):
    """
    Generates a list of urls for the given queries to allrecipes.com, writing them to "urls.txt"

    Args:
        queries (list): A list of strings to search for on allrecipes.com
    Returns:
        None
    """
    urlSet = set()
    for ind, query in enumerate(queries):
        print(f"Generating urls for {query} ({ind + 1}/{len(queries)})")
        search_query = query.replace(" ", "+")
        search_url = f"https://www.allrecipes.com/search?q={search_query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", {"class": "mntl-card-list-items"})
        for link in links:
            url = link['href']
            if "https://www.allrecipes.com/recipe/" in url:
                urlSet.add(url)
    

    with open("urls.txt", "w") as f:
        for url in urlSet:
            f.write(f"{url}\n")

    return list(urlSet)

def generateVerbs(urls):

    verbDict = defaultdict(int)
    for ind, url in enumerate(urls):
        print(f"[{((ind+1)/len(urls))*100:.2f}%] Generating verbs for {url} ({ind + 1}/{len(urls)})")
        scraper = scrape_me(url)
        instructions = scraper.instructions()
        instructions = instructions.replace("\n", "")
        instructions = re.sub(r"(?<![0-9])\.(?![0-9])",". ",instructions)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(instructions)
        for sent in doc.sents:
            root = sent.root
            if root.pos_ == "VERB" and root.text[0].isupper():
                verbDict[root.text] += 1
        
    with open("verbs.txt","w",newline="") as f:
        # sort verbDict by value decreasing
        verbDict = dict(sorted(verbDict.items(), key=lambda item: item[1], reverse=True))
        for verb in verbDict.keys():
            f.write(verb + "\n")

def readUrlsIntoList(urlPath):
    """
    Reads urls from a text file and returns them as a list

    Args:
        urlPath (str): The path to the text file containing urls
    Returns:
        urls (list): A list of urls
    """
    urls = []
    with open(urlPath, "r") as f:
        for line in f:
            urls.append(line.strip())
    return urls
            

if __name__ == "__main__":
    search_queries = [    "chicken",    "beef",    "pork",    "seafood",    "vegetarian",    "vegan",    "gluten-free",    "low-carb",    "low-calorie",    "quick and easy",    "slow cooker",    "instant pot",    "meal prep",    "meal planning",    "budget-friendly",    "one-pot",    "sheet pan",    "grilling",    "roasting",    "baking",    "soup",    "salad",    "pasta",    "pizza",    "sandwich",    "burger",    "taco",    "burrito",    "stir fry",    "curry",    "stew",    "chili",    "casserole",    "lasagna",    "enchilada",    "potato",    "rice",    "quinoa",    "oatmeal",    "smoothie",    "juice",    "cocktail",    "dessert",    "cookie",    "cake",    "pie",    "brownie",    "ice cream",    "chocolate",    "pumpkin",    "apple",    "banana",    "strawberry",    "blueberry",    "lemon",    "lime",    "garlic",    "onion",    "tomato",    "spinach",    "kale",    "broccoli",    "cauliflower",    "zucchini",    "carrot",    "sweet potato",    "butternut squash",    "avocado",    "mushroom",    "eggplant",    "pepper",    "jalapeno",    "cheese",    "yogurt",    "milk",    "cream",    "butter",    "oil",    "vinegar",    "salt",    "pepper",    "sugar",    "honey",    "maple syrup",    "soy sauce",    "hot sauce",    "bbq sauce",    "mayonnaise",    "mustard",    "ketchup",    "sriracha",    "pesto",    "salsa",    "hummus",    "guacamole",    "tahini",    "stock",    "broth",    "wine",    "beer",    "coffee",    "tea",    "lemonade",    "iced tea"]
    # generateUrls(search_queries)
    urls = readUrlsIntoList("urls.txt")
    generateVerbs(urls)


