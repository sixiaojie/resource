import influxdb
import time,os
import configparser


class Base(object):
    def __init__(self,configfile="config/conf.ini",dbname="falcon"):
        self.configfile = configfile
        self.parser = self.configparser()
        self.dbname = dbname
        self.client = influxdb.InfluxDBClient(self.parser.get("server","host"),self.parser.getint("server","port"),self.parser.get("server","username"),self.parser.get("server","password"),self.dbname)

    def configparser(self):
        if os.path.exists(self.configfile) is False:
            self.configfile = "../config/conf.ini"
        cf = configparser.ConfigParser()
        cf.read(self.configfile)
        return cf

    def average(self,metricname="cpu",group=None,host=None):
        if group is None and host is None:
            sql = "select mean(*) from "+metricname
        if group is None and host is not None:
            sql = "select mean(*) from "+metricname+" where \"hostname\" = '%s'" %(host)
        if group is not None and host is None:
            sql = "select mean(*) from "+metricname+" where \"groupname\" = '%s'" %(group)
        if group is not None and host is not None:
            sql = "select mean(*) from " + metricname + " where \"groupname\" = '%s' and \"hostname\" = '%s'" % (group,host)

    def write(self):
        pass

    def execute(self,sql):
        try:
            data = self.client.query(sql).raw
        except Exception as e:
            print(str(e))
            data = None
        return data


if __name__ == "__main__":
    b = Base()
    print(b.parser.get("cpu","threshold"))
