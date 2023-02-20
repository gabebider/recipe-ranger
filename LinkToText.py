import requests
from bs4 import BeautifulSoup
import sys
import re
from RecipeFinder import RecipeFinder

def LinkToText(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    directions_section = soup.find("div", {"id": "recipe__steps_1-0"})
    steps = directions_section.find_all("li")

    step_num = 1
    for step in steps:
        # step.find("p")
        print(f"Step {step_num}: {step.find('p').text.strip()}")
        step_num += 1

if __name__ == "__main__":
    url = RecipeFinder()
    LinkToText(url)

