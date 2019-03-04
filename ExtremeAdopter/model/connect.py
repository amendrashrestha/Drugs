__author__ = 'amendrashrestha'

from pymysql import connect, cursors

def conn_db():
    db = connect(host='localhost', port=8889, user='root', password='root86', db='Flashback', autocommit=True)
    cur = db.cursor(cursors.DictCursor)
    return cur