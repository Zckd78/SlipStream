

def CountElements(string):
    elemFound = False
    elemCount = 0
    for char in string:
        if(char == '<'):
            elemFound = True
        if(elemFound and char == '>'):
            elemCount  += 1
    return elemCount