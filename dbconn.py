import pymysql

class database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='ssuzyn', password='annie1004', db='voice', charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def signup(self, id, pwd):
        sql = "insert into user (id, pwd) values (%s, %s)"
        value = (id, pwd)
        self.cursor.execute(sql, (id, pwd))
        self.db.commit()
        self.db.close()