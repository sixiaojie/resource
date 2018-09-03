import pymysql
from base import base

class Mysql(object):
    def __init__(self):
        self.db = self._connect()

    def _connect(self):
        conf = base.Base()
        db = pymysql.connect(host=conf.parser.get("mysql","host"), user=conf.parser.get("mysql","username"), password=conf.parser.get("mysql","password"), db=conf.parser.get("mysql","dbname"), port=conf.parser.getint("mysql","port"))
        return db

    def closed(self):
        self.db.close()

    def write(self,sql):
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as e:
            print(str(e))
            self.db.rollback()

    def read(self,sql):
        cur = self.db.cursor()
        result = []
        try:
            cur.execute(sql)
            for row in cur.fetchall():
                result.append(row)
        except Exception as e:
            print(str(e))
        return result

