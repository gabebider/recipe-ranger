
class Parse:
    def __init__(self, verb:str, dobj_nouns:list,modifiers:list):
        self.verb = verb
        # TODO: this should classify ingredients and tools differently
        self.dobj_nouns = dobj_nouns
        self.modifiers = modifiers

    def __str__(self):
        return f"Verb: {self.verb}\nDirect Objects: {self.dobj_nouns}\nModifiers: {self.modifiers}"



    
