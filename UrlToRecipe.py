import requests
from bs4 import BeautifulSoup
import sys
import re
from RecipeFinder import RecipeFinder
from Ingredient import Ingredient

def UrlToRecipe(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    directions_section = soup.find("div", {"id": "recipe__steps_1-0"})
    steps = directions_section.find_all("li")
    ingredients_section = soup.find('ul', {'class': 'mntl-structured-ingredients__list'})
    ingredients_list = ingredients_section.find_all('li')
    print()
    print("You will need the following ingredients:")

    # TODO: This does not always scrape ingredients correctly
    # if the recipe has different `sections` of ingredients, it will only get the first part
    # example: https://www.allrecipes.com/recipe/70935/taqueria-style-tacos-carne-asada/
    # TODO: fix this... probably check for other sections or something, have to look at HTML
    # code to know for sure
    
    for ingredient in ingredients_list:
        sections = ingredient.find_all("span")
        newIngredient = Ingredient()
        for section in sections:
            if 'data-ingredient-quantity' in section.attrs:
                newIngredient.setQuantity(section.text.strip())
            elif 'data-ingredient-unit' in section.attrs:
                newIngredient.setUnit(section.text.strip())
            elif 'data-ingredient-name' in section.attrs:
                newIngredient.setName(section.text.strip())
        print(newIngredient.printBreakdown())

    # step_num = 1
    # for step in steps:
    #     # step.find("p")
    #     print(f"Step {step_num}: {step.find('p').text.strip()}")
    #     step_num += 1

if __name__ == "__main__":
    url = RecipeFinder()
    UrlToRecipe(url)

