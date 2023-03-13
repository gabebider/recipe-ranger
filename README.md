# Recipe Ranger - Project 3

<img src="./logo.png" width="200px">

---

## Installation

You first need to install the dependencies for the project. You can do this on macOS by running the following command (not needed for Windows):

```bash
brew install portaudio
```

Then, you can install the Python dependencies by running the following command (Both macOS and Windows):

```bash
pip install -r requirements.txt
```

---

## Running

To run the project, you can run the following command after installing the dependencies:

```bash
python Runner.py
```

That will let you choose between providing a recipe or searching for one. If you choose to provide a recipe, you will asked to provide a link to a recipe. If you choose to ask for a recipe, you will be asked to provide a keyword to search for, and then choose a recipe from the results.

---

## Assigned Tasks

### Project 3

- [x] Accept the URL of a recipe from AllRecipes.com, and programmatically fetch the page.
- [x] Parse it into the recipe data representation your group designs. Your parser should be able to recognize:
  - [x] Ingredients
    - [x] Ingredient name
    - [x] Quantity
    - [x] Measurement (cup, teaspoon, pinch, etc.)
    - [x] (optional) Descriptor (e.g. fresh, extra-virgin)
    - [x] (optional) Preparation (e.g. finely chopped)
  - [x] Tools – pans, graters, whisks, etc.
  - [x] Methods
    - [x] Primary cooking method (e.g. sauté, broil, boil, poach, etc.)
    - [ ] (optional) Other cooking methods used (e.g. chop, grate, stir, shake, mince, crush, squeeze, etc.)
  - [x] Steps – parse the directions into a series of steps that each consist of ingredients, tools, methods, and times
- [x] Ask the user what kind of transformation they want to do.
  - [x] To and from vegetarian (REQUIRED)
  - [x] To and from healthy (REQUIRED)
  - [x] Style of cuisine (AT LEAST ONE REQUIRED) - Mexican
  - [x] Additional Style of cuisine (OPTIONAL) - Indian
  - [x] Double the amount or cut it by half (OPTIONAL)
  - [ ] Cooking method (from bake to stir fry, for example) (OPTIONAL)
  - [x] Gluten- or lactose-free (OPTIONAL) - Both gluten and lactose free

### Project 2

- [X] Recipe retrieval and display (see example above, including "Show me the ingredients list");
- [X] Navigation utterances ("Go back one step", "Go to the next step", "Repeat please", "Take me to the 1st step", "Take me to the n-th step");
- [X] Vague "how to" questions ("How do I do that?", in which case you can infer a context based on what's parsed for the current step);
- [X] Specific "how to" questions ("How do I <specific technique>?");
- [X] Simple "what is" questions ("What is a <tool being mentioned>?");
- [X] Asking about the parameters of the current step ("How much of <ingredient> do I need?", "What temperature?", "How long do I <specific technique>?", "When is it done?");
- [X] Ingredient substitution questions ("What can I substitute for <ingredient>?");
- [X] Name your bot :) - Recipe ranger

## Extra

We made our chat bot voice to text so you can interact with it. This video can be viewed from the google folder linked in the canvas comment. To enable voice to text, navigate to runner.py. On line 281, change voice=False to voice=True.

---

## Authors

By Spencer Rothfleisch, Gabe Bider, Eli Barlow and Isaac Miller

## Github Link

View the GitHub Repository [here](https://github.com/gabebider/cs337-proj2)
