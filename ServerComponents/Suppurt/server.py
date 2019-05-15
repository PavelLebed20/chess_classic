import psycopg2

password = 'c6b476253566b10c0a2fde6065a836ad587be943e05e56ae24cd55dd0f95901e'
user = 'nglyhlqtzgflza'
host = 'ec2-54-247-72-30.eu-west-1.compute.amazonaws.com'
database = 'd6veee8q9722ca'
port = '5432'

def execute_no_res_async(query):
    try:
        con = psycopg2.connect(user=user,
                               password=password,
                               host=host,
                               port=port,
                               database=database)
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
        con = psycopg2.connect(user=user,
                               password=password,
                               host=host,
                               port=port,
                               database=database)
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
        con = psycopg2.connect(user=user,
                               password=password,
                               host=host,
                               port=port,
                               database=database)
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
