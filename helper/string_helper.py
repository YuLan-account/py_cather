

def isBlank(myString):
    if myString and myString.strip():
        # myString is not None AND myString is not empty or blank
        return False
        # myString is None OR myString is empty or blank
    return True


def isNotBlank(str):
    if str and str.strip():
        return True

    return False