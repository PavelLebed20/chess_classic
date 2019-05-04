

import psycopg2

class db:
    def __init__(self):
        try:
            self.con = psycopg2.connect(user = "postgres",
                                          password = "postgres",
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "chess")
            self.con.autocommit = True
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)



def getParamsValMap(data):
    paramsVal = str(data).split('&')
    res = {}

    for paramVal in paramsVal:
        paramToVal = str(paramVal).split('=')
        res.update({paramToVal[0]: paramToVal[1]})
    return res

def deleteKeyByVal(dict, find_val):
    for key, val in dict.items():
        if (val == find_val):
            dict.pop(key)

def getkeyByVal(dict, find_val):
    for key, val in dict.items():
        if (val == find_val):
            return key
    return None