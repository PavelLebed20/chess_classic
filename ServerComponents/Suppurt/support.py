def getParamsValMap(data):
    paramsVal = str(data).split('&')
    res = {}

    for paramVal in paramsVal:
        paramToVal = str(paramVal).split('=')
        res.update({paramToVal[0]: paramToVal[1]})
    return res
