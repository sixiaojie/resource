#encoding:utf-8
from base import base
from base import db
from base import common
import redis

current = common.current
last = common.last_month
current_influxdb = common.current_month_influxdb

def SecondBiz_info():
    sql = "select count(*) from cpu"

class Action(object):
    def __init__(self):
        self.client = base.Base()
        self.metrics = self.client.parser.get("server", "monitor")
        self.db = self._mysql()
        self.red = self._redis()

    def cmdb_rsync_redis(self):
        data = self.db.read("select * from biz_info")
        for item in data:
            print(item)
            self.red.set(item[4],item[0])


    def _mysql(self):
        return db.Mysql()

    def _redis(self):
        return  redis.Redis(host='127.0.0.1')

    ##这里阈值和实际取到的进行对比
    def Threshold(self):
        self.db.write("truncate threshold_%s" %current)
        self.db.write("truncate gthreshold_%s" %current)
        group_count = {}
        for metric in self.metrics.split(","):
            threshold = self.client.parser.get(metric,"threshold")
            subtract = self.client.parser.getboolean(metric,"subtract")
            if subtract:
                sql = "select min(value) from \"%s\" group by endpoint" % (metric)
            else:
                sql = "select max(value) from \"%s\" group by endpoint" %(metric)
            data = self.client.execute(sql)
            if data is None:
                continue
            for item in data["series"]:
                if subtract:
                    if item["values"][0][1] <(100-int(threshold)):
                        continue
                else:
                    if item["values"][0][1] > int(threshold):
                        continue
                sql = "select * from threshold_%s where hostname='%s' and metric='%s'" %(current,item["tags"]["endpoint"],metric)
                result = self.db.read(sql)
                if len(result) == 0:
                    groupname = self.red.get(item["tags"]["endpoint"]).decode('utf-8')
                    sql = "insert into threshold_%s(metric,hostname,groupname,minvalue,hostnamecount) VALUES ('%s','%s','%s',%f,%d)" %(current,metric,item["tags"]["endpoint"],groupname,item["values"][0][1],1)
                    self.db.write(sql)
                    if group_count.get(groupname) is None:
                        group_count[groupname] = {item["tags"]["endpoint"]:{"metric":[metric]}}
                    else:
                        if group_count[groupname].get(item["tags"]["endpoint"]) is None:
                            group_count[groupname][item["tags"]["endpoint"]] = {"metric": [metric]}
                        else:
                            group_count[groupname][item["tags"]["endpoint"]]["metric"].append(metric)
        ##这里得到业务组有哪些机器资源空闲，且空闲是哪些监控值
        for item in group_count:
            aa = {}
            count = len(group_count[item])
            metric_info = ""
            for hostname in group_count[item]:
                for metric in group_count[item][hostname]["metric"]:
                    if aa.get(metric):
                        continue
                    else:
                        aa[metric] = "test"
            length = len(aa)
            i = 0
            for metric in aa:
                if i == length -2:
                    metric_info += metric
                else:
                    metric_info += metric+","
            sql = "select * from gthreshold_%s where groupname ='%s'" %(current,item)
            if len(self.db.read(sql)) == 0:
                sql = "insert into gthreshold_%s(metric,groupname,groupnamecount) VALUES ('%s','%s',%d)" %(current,metric_info,item,count)
                self.db.write(sql)

    def __del__(self):
        self.db.closed()

    def biz_info(self):
        self.db.write("truncate groupnamecount_%s" %current)
        Msql = "select firstname,firstfullname,count(*) from biz_info_%s group by firstname" %current
        result = self.db.read(Msql)
        for row in result:
            if row[0] == "":
                groupname="unbind"
                groupfullname = "未绑定机器"
            else:
                groupname= row[0]
                groupfullname = row[1]
            Msql = "insert into groupnamecount_%s(groupname,groupfullname,count) values('%s','%s',%d)" %(current,groupname,groupfullname,row[2])
            self.db.write(Msql)

    ##这里得到机器数量差值
    def increment(self):
        sql = "select count(*) from groupnamecount_%s" %last
        if len(self.db.read(sql)) == 0:
            pass
        sql = "insert into increment select t2.groupname,t2.groupfullname,(t2.count - t1.count) as `count` from groupnamecount_%s as t1, groupnamecount_%sas t2 where t1.id=t2.id;" %(last,current)
        self.db.write(sql)
        sql = "insert into increment select groupname,groupfullname,`count` from groupnamecount_%s where groupname not in (select groupname from increment);" %current
        self.db.write(sql)

    def aggressive(self):
        self.db.write("truncate host_aggres_%s" %current)
        self.db.write("truncate group_aggres_%s" % current)
        Isql = "select mean(*) from \"cpu.idle_aggres\" where \"month\" =~ /%s/ group by hostname,hours limit 1" %(current_influxdb)
        client = base.Base(dbname="mydb")
        data = client.execute(Isql)
        for item in data["series"]:
            sql = "insert into host_aggres_%s(hostname,avg_value,max_value,min_value,`current`) values('%s',%f,%f,%f,'%s')" %(current,item["tags"]["hostname"],round(float(item["values"][0][1]),2),round(float(item["values"][0][2]),2),round(float(item["values"][0][3]),2),item["tags"]["hours"])
            self.db.write(sql)
        Isql = "select mean(*) from \"cpu.idle_aggres\" where \"month\" =~ /%s/ group by groupname,hours limit 1" %(current_influxdb)
        data = client.execute(Isql)
        for item in data["series"]:
            sql = "insert into group_aggres_%s(hostname,avg_value,max_value,min_value,`current`) values('%s',%f,%f,%f,'%s')" %(current,item["tags"]["groupname"],round(float(item["values"][0][1]),2),round(float(item["values"][0][2]),2),round(float(item["values"][0][3]),2),item["tags"]["hours"])
            self.db.write(sql)

    def Copy_table_common(self):
        table_name=["host_aggres","threshold","gthreshold","biz_info","groupnamecount","group_aggres"]
        for item in table_name:
            self.db.write("drop table %s" % item)
            self.db.write("create table %s select * from %s_%s" % (item, item, current))

    def D_value(self):
        print(111)
        self.db.write("truncate D_value")
        self.db.write("insert into D_value(hostname,value,current) select hostname,(max_value-min_value) as D_value,current from host_aggres order by D_value desc;")


if __name__ == "__main__":

    action = Action()
    action.cmdb_rsync_redis()
    action.Threshold()

