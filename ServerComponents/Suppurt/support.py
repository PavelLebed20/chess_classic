def getParamsValMap(data):
    paramsVal = str(data).split('&')
    res = {}

    for paramVal in paramsVal:
        paramToVal = str(paramVal).split('=')
        if len(paramToVal) > 1:
            data = paramToVal[1]
        else:
            data = None
        res[paramToVal[0]] = data if data != '' else None
    return res
