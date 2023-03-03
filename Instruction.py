import spacy
class Instruction:
    def __init__(self,text):
        self.text = text

    def __str__(self):
        return self.text
    
    def parseText(self):
        nlp = spacy.load("en_core_web_md")
        #! nlp.add_pipe("merge_noun_chunks")
        doc = nlp(self.text)
        pass
        #TODO: implement this function --> should set some attributes of the instruction object
        # such as the main verb, the noun(s) that verb acts on, and the modifiers on the verb
        # ex: "Preheat the oven to 350 degrees F (175 degrees C)."
        # main verb: "Preheat"
        # noun(s): "oven"
        # modifiers: "to 350 degrees F (175 degrees C)"
        # so that we can later ask "what temperature should I preheat to?" and get "350 degrees F (175 degrees C)"

    
