import psycopg2


def execute_no_res_async(query):
    try:
        con = psycopg2.connect(user="postgres",
                               password="postgres",
                               host="127.0.0.1",
                               port="5432",
                               database="chess")
        con.autocommit = True

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return
    cursor = con.cursor()
    cursor.execute(query)
    cursor.close()
    con.close()


def execute_one_res_async(query):
    try:
        con = psycopg2.connect(user="postgres",
                               password="postgres",
                               host="127.0.0.1",
                               port="5432",
                               database="chess")
        con.autocommit = True

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return
    cursor = con.cursor()
    cursor.execute(query)
    res = cursor.fetchone()
    cursor.close()
    con.close()
    return res


def execute_all_res_async(query):
    try:
        con = psycopg2.connect(user="postgres",
                               password="postgres",
                               host="127.0.0.1",
                               port="5432",
                               database="chess")
        con.autocommit = True

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return
    cursor = con.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    con.close()
    return res
