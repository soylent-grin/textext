indexToLocationType = {
    1: "location city",
    2: "location country",
    3: "foundation place",
    4: "headquarted location"
}

def constructDecision(locationType, isTrue):
    return str(locationType) + "." + str(1 if isTrue else 0)

def parseDecision(code):
    parts = code.split(".")
    locationType = indexToLocationType[int(parts[0])]
    decision = "true" if (int(parts[1]) == 1) else "false"
    return "{0} - {1}".format(locationType, decision)

def parseDecisionResult(code):
    parts = code.split(".")
    return int(parts[1]) == 1

def parseDecisionLabel(code):
    parts = code.split(".")
    return indexToLocationType[int(parts[0])]