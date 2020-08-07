#!/bin/python3

##################################################
# log something
def log(msg):
    print('[kafka_helper] ' + msg)
    #logger.info('[kafka_helper] ' + msg)

##################################################
# Safely convert to string.
# If the input is None, return None, else convert via str().
# This is needed because robot uses ustrings.
def toStr(inputString):
    if None == inputString:
        return None
    elif isinstance(inputString, str):
        return inputString
    elif isinstance(inputString, unicode):
        return inputString.encode("utf-8")
    else:
        # not a string
        return None

    return inputString.encode("utf-8")


##################################################
# Convert an input string to unicode
# If the input is None, return None, else convert via str().
def toUnicode(inputString):
    if None == inputString:
        return None
    elif isinstance(inputString, str):
        return unicode(inputString, "utf-8")
    elif isinstance(inputString, unicode):
        return inputString
    else:
        # not a string
        return None

