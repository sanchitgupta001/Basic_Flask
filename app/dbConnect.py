import MySQLdb

def connection():
    conn = MySQLdb.connect(host = "localhost",
                           user = "root",
                           passwd = "",
                           db = "Register")
    c = conn.cursor()

    return c, conn                       
