import re

previousWords = [
    "previous",
    "back",
    "previous step",
    "previous page",
    "last step",
    "go back",
    "go to the previous step",
    "step before",
    "prior step"
]

nextWords = [
    "next",
    "continue",
    "okay",
    "ok",
    "next step",
    "forward",
    "move on",
    "continue to the next step",
    "next page",
    "proceed",
    "next action",
    "advance"
]

repeatWords = [
    "repeat",
    "repeat step",
    "repeat previous step",
    "one more time",
    "do it again",
    "redo",
    "retry",
    "restart",
    "replay",
    "loop back",
    "repeat the process"
]

specificStepWords = [
    'take me',
    'go to',
    'want to see',
    'show me'
]

allStepsWords = [
    'all the steps',
    'all the instructions',
    'all the directions',
    'all the steps of the recipe',
    'show me all', 
]
ordinal_numbers = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
    "twenty-first": 21,
    "twenty-second": 22,
    "twenty-third": 23,
    "twenty-fourth": 24,
    "twenty-fifth": 25,
    "twenty-sixth": 26,
    "twenty-seventh": 27,
    "twenty-eighth": 28,
    "twenty-ninth": 29,
    "thirtieth": 30,
    "thirty-first": 31,
    "thirty-second": 32,
    "thirty-third": 33,
    "thirty-fourth": 34,
    "thirty-fifth": 35,
    "thirty-sixth": 36,
    "thirty-seventh": 37,
    "thirty-eighth": 38,
    "thirty-ninth": 39,
    "fortieth": 40,
    "forty-first": 41,
    "forty-second": 42,
    "forty-third": 43,
    "forty-fourth": 44,
    "forty-fifth": 45,
    "forty-sixth": 46,
    "forty-seventh": 47,
    "forty-eighth": 48,
    "forty-ninth": 49,
    "fiftieth": 50
}

number_names = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    21: "twenty-one",
    22: "twenty-two",
    23: "twenty-three",
    24: "twenty-four",
    25: "twenty-five",
    26: "twenty-six",
    27: "twenty-seven",
    28: "twenty-eight",
    29: "twenty-nine",
    30: "thirty",
    31: "thirty-one",
    32: "thirty-two",
    33: "thirty-three",
    34: "thirty-four",
    35: "thirty-five",
    36: "thirty-six",
    37: "thirty-seven",
    38: "thirty-eight",
    39: "thirty-nine",
    40: "forty",
    41: "forty-one",
    42: "forty-two",
    43: "forty-three",
    44: "forty-four",
    45: "forty-five",
    46: "forty-six",
    47: "forty-seven",
    48: "forty-eight",
    49: "forty-nine",
    50: "fifty"
}

def tokenize(text: str) -> list:
	""" 
	Given a string, return a list of the lowercase tokens (words) in that string

    Parameters:
        text (str): The string to be tokenized

    Returns:    
        list: A list of the lowercase tokens (words) in the string
	"""
	# Split this text on any whitespace, then for each section
	# * remove any non alphabetic character ([^A-Za-z])
	# * convert to lowercase
	# * strip away any extra whitespace
	tokens = [re.sub(r'[^A-Za-z]+', '', s).lower().strip() for s in  text.split()]
	return tokens

def isNavigation(text: str) -> bool:
    allWords = previousWords + nextWords + repeatWords + specificStepWords + allStepsWords
    if any(word in text for word in allWords):
        return True
    return False

def doNavigation(text: str, step: int) -> int:
    # check if asking for specific step
    text = text.lower().strip()

    if any( word in text for word in specificStepWords):
        step_request = re.search(r'\d+', text)
        if step_request:
            step_request = int(step_request.group())
            return step_request
        
    tokens = tokenize(text)
    for token in tokens:
        if token in ordinal_numbers:
            return ordinal_numbers[token]
        elif token in number_names:
            return number_names[token]

    if any(word in text for word in previousWords):
        return step - 1
    elif any(word in text for word in nextWords):
        return step + 1
    else:
        return step


def isAllSteps(text: str) -> bool:
    if any((word in text and not "ingredient" in text) for word in allStepsWords):
        return True
    return False

def isAllIngredients(text: str) -> bool:
    if any((word in text and "ingredient" in text) for word in allStepsWords):
        return True
    return False
