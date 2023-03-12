# Recipe Ranger - Project 3
<img src="./logo.png" width="200px">

---

## Installation
You first need to install the dependencies for the project. You can do this on macos by running the following command:

```bash
brew install portaudio
```

Then, you can install the Python dependencies by running the following command:

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
## Tasks
- [X] Recipe retrieval and display (see example above, including "Show me the ingredients list");
- [X] Navigation utterances ("Go back one step", "Go to the next step", "Repeat please", "Take me to the 1st step", "Take me to the n-th step");
- [X] Vague "how to" questions ("How do I do that?", in which case you can infer a context based on what's parsed for the current step);
- [X] Specific "how to" questions ("How do I <specific technique>?");
- [X] Simple "what is" questions ("What is a <tool being mentioned>?");
- [X] Asking about the parameters of the current step ("How much of <ingredient> do I need?", "What temperature?", "How long do I <specific technique>?", "When is it done?");
- [X] Ingredient substitution questions ("What can I substitute for <ingredient>?");
- [X] Name your bot :) - Recipe ranger

## Tasks
We made our chat bot voice to text so you can interact with it. This video can be viewed from the google folder linked in the canvas comment. To enable voice to text, navigate to runner.py. On line 281, change voice=False to voice=True.

---
## Authors
By Spencer Rothfleisch, Gabe Bider, Eli Barlow and Isaac Miller
