import requests
from bs4 import BeautifulSoup
import sys
import re

if len(sys.argv) > 1:
    recipe_request = sys.argv[1]
    # recipe_request = input("What type of recipe would you like to cook?: ")
else:
    recipe_request = input("What type of recipe would you like to cook?: ")

# normalize the input
# probably need to stop the user from inputting some bad stuff like numbers or others
recipe_request = recipe_request.lower().strip() 
recipe_request.replace(" ", "+") # replace spaces with pluses for url

# search for the recipe on AllRecipescom
search_url = f"https://allrecipes.com/search?q={recipe_request}"
search_response = requests.get(search_url)
search_soup = BeautifulSoup(search_response.text, "html.parser")
search_list = search_soup.find("div", {"id": "card-list_1-0"}) # find the section of recipes
search_a_tags = search_list.find_all("a")  # find all the links to recipes
search_recipes = []
for a_tag in search_a_tags:
    title = a_tag.text.strip() # remove leading and trailing whitespace
    title = title.replace("\n", " ") # relplace newlines with spaces
    title = title.replace(",", "") # remove commas
    title = re.sub(' +', ' ', title) # remove extra spaces
    title = re.sub(r'\s[0-9]+\sRatings', '', title) # remove ratings
    title = title.replace("Save ", "") # remove "Save" from the beginning of the title
    search_recipes.append((title, a_tag["href"])) # add the title and url to the list

# Now we have a list of tuples with the recipe name and the url
# index 0 is the first search result, index 1 is the second, etc.
if len(search_recipes) <= 5:
    option_number = 1
    for option in search_recipes:
        print(f"({option_number}) {option[0]}")
        option_number += 1
    recipe_choice = input("Which recipe would you like to cook?: ")
    while recipe_choice not in ["1", "2", "3", "4", "5"]:
        recipe_choice = input("Please select a recipe number from 1 to 5: ")
    recipe_choice = int(recipe_choice) - 1
else:
    option_number = 1
    limit = 5
    LIMIT_INCREMENT = 5
    i = 0
    choices = set()
    # paginate the results 5 at a time
    while True:
        while i < len(search_recipes):
            if i < limit:
                # print the recipe name and number
                print(f"({option_number}) {search_recipes[i][0]}")
                choices.add(option_number)  
                option_number += 1
                i += 1
            else:
                print(f"({option_number}) Next 5 results")
                choices.add(option_number)
                page_num_choice = option_number
                option_number += 1
                i += 1
                break
        recipe_choice = input("Which recipe would you like to cook?: ")
        # validate the input as a number
        while not recipe_choice.isdigit():
            recipe_choice = input("Please enter a valid number: ")
        # validate the input as a number in the choices
        while int(recipe_choice) not in choices:
            recipe_choice = input("Please enter a valid number: ")
        # if the user chose the next 5 results, increment the limit and continue
        if int(recipe_choice) == page_num_choice:
            limit += LIMIT_INCREMENT
            continue
        # otherwise we have a valid choice
        else:
            recipe_choice = int(recipe_choice) - 1
            break

print(f"Yum! You chose: {search_recipes[recipe_choice][0]}")
print(f"Requesting recipe from {search_recipes[recipe_choice][1]}")
# Now we have the recipe choice
recipe_url = search_recipes[recipe_choice][1]
