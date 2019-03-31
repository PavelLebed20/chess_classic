import pyodbc


class db:

    def __init__(self):
        self.db_ip = "192.168.1.1"
        self.db_name = "Chess"
        self.db_user = ""
        self.db_password = ""

        cnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=" + self.db_ip +
                              ";DATABASE=" + self.db_name + ";UID=" + self.db_user + ";PWD=" + self.db_password)
        self.cursor = cnxn.cursor()

    def request(self, request):
        if (self.cursor == None):
            return None
        return self.cursor.execute(request)

