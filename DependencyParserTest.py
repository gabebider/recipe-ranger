import spacy
from spacy import displacy
from recipe_scrapers import scrape_me
import textacy
import subprocess

str1 = "Preheat the oven to 350 degrees F (175 degrees C)."
str2 = "Lightly grease a large baking sheet with cooking spray."
str3 = "Whisk soy sauce, agave, sesame oil, garlic, and ginger together in a bowl until evenly combined."

def ParseDependency(s=str1):
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("merge_noun_chunks")
    doc = nlp(s)
    html = displacy.render(doc, style="dep",options={"dep":True})
    with open("parse2.html", "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run(["open", "parse2.html"], check=True)
    
link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

if __name__ == '__main__':
    ParseDependency(str3)