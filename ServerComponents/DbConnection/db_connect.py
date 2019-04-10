import psycopg2

class db:
    def __init__(self):
        try:
            self.con = psycopg2.connect(user = "postgres",
                                          password = "postgres",
                                          host = "127.0.0.1",
                                          port = "5432",
                                          database = "chess")
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)


#db_ = db()
#cur = db_.con.cursor()
#cur.execute("select * from chess.message_types")
#record = cur.fetchone()
#print(record[0])

