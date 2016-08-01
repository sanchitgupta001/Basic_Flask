import MySQLdb

def connection():
    conn = MySQLdb.connect(host = "localhost",
                           user = "root",
                           passwd = "",
                           db = "Users",unix_socket="/opt/lampp/var/mysql/mysql.sock")
    c = conn.cursor()

    return c, conn
