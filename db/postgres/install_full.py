#########################################
# MODULE: Install database environment  #
# AUTHOR: Lebed' Pavel                  #
# LAST UPDATE: 10/04/2019               #
#########################################
import os

import psycopg2


class DatabaseInstaller:
    con = None

    def __init__(self, dbname, user_name, host, password, port):
        try:
            self.con = psycopg2.connect(dbname='postgres',
                                        user=user_name, host=host,
                                        password=password, port=port)
            self.con.autocommit = True
            cursor = self.con.cursor()
            cursor.execute('DROP DATABASE IF EXISTS {}'.format(dbname))
            cursor.execute('CREATE DATABASE {}'.format(dbname))
            cursor.close()
            self.con.close()

            self.con = None

            self.con = psycopg2.connect(password=password, user=user_name,
                                        host=host, database=dbname, port=port)
            self.con.autocommit = True

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)


db = DatabaseInstaller(dbname='chess', user_name='postgres',
                       host='localhost', password='postgres', port='5432')

dir_path = os.path.dirname(os.path.abspath(__file__))


def execute_file(script_file_name):
    if db.con is None:
        return
    db.con.autocommit = True
    cursor = db.con.cursor()
    with open(dir_path + '/' + script_file_name, 'r') as query_file:
        query = query_file.read()
        cursor.execute(query)
    cursor.close()


execute_file('SCH/tables_full.sql')

execute_file('SCH/tables_data.sql')

api_files = []
for r, d, f in os.walk(dir_path + '/API/'):
    for file in f:
        api_files.append(os.path.join(file))

for file in api_files:
    execute_file('API/{0}'.format(file))


