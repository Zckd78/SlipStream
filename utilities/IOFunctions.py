import io
import os
import datetime

def LoadFileContents(filename:str):
    raw = ""
    try:
        with io.open(filename, 'r', encoding='utf8') as file:
            print("Opening iTunes Library XML: " + filename)
            raw = file.read()
    except IOError as ioerr:
        print(" Error in IOFunctions : " + str(ioerr))
    return raw

def SaveLog(outputLog):
    folder = os.getcwd() + "\\" + "OutputLog"
    if not os.path.exists(folder):
        os.mkdir(folder)

    destFile = MergePaths(folder, "Output_" + str(datetime.date.today()) + ".log" )
    try:
        with io.open(destFile, 'w', encoding='utf8') as file:
            print("Saving output log to: " + destFile)
            file.write(outputLog)
    except IOError as ioerr:
        print(" Error in IOFunctions : " + str(ioerr))


def MergePaths(path1, path2):
    return path1 + "\\" + path2
