import requests


def SplitElements(string):
    elemFound = False
    elemTyped = False
    elemType = ""
    elemArray = {'':''}
    elemPart = ""

    for char in string:
        if(elemFound and not elemTyped):
            if(char != " "):
                elemType += char
            else:


        if(elemFound and char != '>'):
            elemPart += char
        if(char == '<'):
            elemFound = True
            elemTyped = True
        if(elemFound and char == '>'):
            elemFound = False
            elemArray.append(elemPart)
            elemPart = ""

    return elemArray


""" Start the main execution """

#inp = input("Enter the URL")

res = requests.get("http://google.com")

count = CountElements(res.text)

array = SplitElements(res.text)


quit()

