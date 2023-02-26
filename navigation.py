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

def isNavigation(text: str) -> bool:
    allWords = previousWords + nextWords + repeatWords
    if any(word in text for word in allWords):
        return True
    return False

def doNavigation(text: str, step: int) -> int:
    if any(word in text for word in previousWords):
        return step - 1
    elif any(word in text for word in nextWords):
        return step + 1
    else:
        return step

