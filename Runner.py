from recipe_scrapers import scrape_me

class Runner():
    def __init__(self):
        # Get the recipe link
        # link = get_recipe_link()
        link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

        # Scrape the recipe page using recipe_scrapers
        scraper = scrape_me(link)

        print(scraper.instructions())
        print(scraper.instructions().split("\n"))
        print("\n")
        print(scraper.ingredients())

        # Split the steps from recipe_scrapers into smaller steps

        # Display step 1 and ask user for input

        # Check if verb is information or navigation

        # If ingredient, then use parser to find ingredient

        # If navigation, then navigate in indicated direction

if __name__ == '__main__':
    Runner()