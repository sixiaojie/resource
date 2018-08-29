from base import base
from base import db

def SecondBiz_info():
    sql = "select count(*) from cpu"

class Action(object):
    def __init__(self):
        self.client = base.Base()
        self.metrics = self.client.parser.get("server", "monitor")
        self.db = self._mysql()

    #这里取得业务机器列表
    def Biz_info(self,name="gruopname"):
        sql = "select count(*) from cpu group by "+name
        return self.client.execute(sql)

    def _mysql(self):
        return db.Mysql()

    ##这里阈值和实际取到的进行对比
    def Threshold(self):
        group_count = {}
        for metric in self.metrics.split(","):
            threshold = self.client.parser.get(metric,"threshold")
            if metric == "established":
                sql = "select max(value) from %s group by groupname,hostname" % (metric)
            else:
                sql = "select min(value) from %s group by groupname,hostname" %(metric)
            data = self.client.execute(sql)
            if data is None:
                continue
            for item in data["series"]:
                if metric == "cpu" or metric == "memory":
                    if item["values"][0][1] <(100-int(threshold)):
                        continue
                else:
                    if item["values"][0][1] > int(threshold):
                        continue
                sql = "insert into threshold(metric,hostname,groupname,minvalue,hostnamecount) VALUES ('%s','%s','%s',%f,%d)" %(metric,item["tags"]["hostname"],item["tags"]["groupname"],item["values"][0][1],1)
                self.db.write(sql)
                if group_count.get(item["tags"]["groupname"]) is None:
                    group_count[item["tags"]["groupname"]] = {item["tags"]["hostname"]:{"metric":[metric]}}
                else:
                    if group_count[item["tags"]["groupname"]].get(item["tags"]["hostname"]) is None:
                        group_count[item["tags"]["groupname"]][item["tags"]["hostname"]] = {"metric": [metric]}
                    else:
                        group_count[item["tags"]["groupname"]][item["tags"]["hostname"]]["metric"].append(metric)
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
                if i == length -1:
                    metric_info += metric
                else:
                    metric_info += metric+","
            sql = "insert into gthreshold(metric,groupname,groupnamecount) VALUES ('%s','%s',%d)" %(item,metric_info,count)
            self.db.write(sql)







action = Action()
action.Threshold()


