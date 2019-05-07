import os
import psycopg2

password = 'c6b476253566b10c0a2fde6065a836ad587be943e05e56ae24cd55dd0f95901e'
user = 'nglyhlqtzgflza'
host = 'ec2-54-247-72-30.eu-west-1.compute.amazonaws.com'
database = 'd6veee8q9722ca'
port = '5432'

class DatabaseInstaller:
    con = None

    def __init__(self, dbname, user_name, host, password, port):
        try:
            self.con = psycopg2.connect(password=password, user=user_name,
                                        host=host, database=dbname, port=port)
            self.con.autocommit = True

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)


db = DatabaseInstaller(dbname=database, user_name=user,
                       host=host, password=password, port=port)

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