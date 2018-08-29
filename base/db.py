import pymysql

class Mysql(object):
    def __init__(self):
        self.db = self._connect()

    def _connect(self):
        db = pymysql.connect(host="localhost", user="root", password="", db="sijie", port=3306)
        return db

    def closed(self):
        self.db.close()

    def write(self,sql):
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    def read(self,sql):
        pass