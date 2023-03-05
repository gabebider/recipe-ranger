import spacy
from spacy import displacy
from recipe_scrapers import scrape_me
import textacy
import subprocess


def ParseDependency(s):
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("merge_noun_chunks")
    doc = nlp(s)
    html = displacy.render(doc, style="dep",options={"dep":True})
    with open("parse2.html", "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run(["open", "parse2.html"], check=True)
    
link = 'https://www.allrecipes.com/recipe/20171/quick-and-easy-pizza-crust/'

if __name__ == '__main__':
    ParseDependency("Whisk together oil and lemon juice for 3 minutes.")