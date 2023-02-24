from recipe_scrapers import scrape_me
from pprint import pprint

class Runner():
    def __init__(self):
        # Get the recipe link
        # link = get_recipe_link()
        link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

        # Scrape the recipe page using recipe_scrapers
        scraper = scrape_me(link)

        # print(scraper.instructions())
        # print(scraper.instructions().split("\n"))
        # print("\n")
        # print(scraper.ingredients())

        # Split the steps from recipe_scrapers into smaller steps
        # steps = self.split_steps(scraper.instructions())
        # pprint(steps)
        ingredients = scraper.ingredients()
        pprint(ingredients)
        # Display step 1 and ask user for input

        # Check if verb is information or navigation

        # If ingredient, then use parser to find ingredient

        # If navigation, then navigate in indicated direction

    def split_steps(self, steps):
        # Split the steps into smaller steps
        steps.replace("\n", "")
        steps.replace("\\n", "")
        print(steps)
        print("\n\n")
        # Replace ". " with "; " to split the steps by periods and semi-colons
        steps.replace(". ", ";")
        intermediateSteps = steps.split(";")
        # Split the individual steps into smaller steps by periods and semi-colons
        steps = []

        
        for i in range(len(intermediateSteps)):
            intermediateSteps = intermediateSteps[i].split("; ")
            intermediateSteps = [item.replace("\n", "") for item in intermediateSteps]
            steps.append(intermediateSteps)


        # Flatten the list
        steps = [item for sublist in steps for item in sublist]
        
        return steps

if __name__ == '__main__':
    Runner()