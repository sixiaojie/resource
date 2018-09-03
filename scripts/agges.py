from influxdb import InfluxDBClient
import redis
import multiprocessing
import sys
import time
from base import base

client = base.Base()

host=[]
l = multiprocessing.Lock()
def lockclient(sql):
    l.acquire()
    data = client.execute(sql)
    l.release()
    return data
a = lockclient("select min(*) from cpu group by groupname,hostname;")
b = {}
for item in a["series"]:
    b[item["tags"]["hostname"]] = item["tags"]["groupname"]
    host.append(item["tags"]["hostname"])
def writefile(i):
    hostname = host[i]
    path = "files/"+hostname+".log"
    groupname = b[hostname]
    item_list = client.parser.get("server","monitor").split(",")
    with open(path,"w+") as f:
      try:
         for item in item_list:
            url = "select mean(*) as avg,min(value),max(value) from %s where \"hostname\"='%s' group by time(60m)" %(item,hostname)
            data = lockclient(url)
            if data.get("series") is None:
                  continue
            for itemdata in data['series'][0]["values"]:
                   if itemdata[3] is  None:
                        continue
                   month = itemdata[0].split("T")[0]
                   hours = itemdata[0].split("T")[1].split("Z")[0]
                   if item == "established":
                        f.write(item+"_aggres,"+"hostname="+hostname+",groupname="+groupname+ ",month=" + month + ",hours=" + hours+" average="+str(itemdata[1])+",maxvalue="+str(itemdata[3])+",minvalue="+str(itemdata[2])+"\n")
                   else:
                        f.write(item + "_aggres," + "hostname=" + hostname + ",groupname=" + groupname + ",month=" + month + ",hours=" + hours+ " average=" + str(100 - itemdata[1]) + ",maxvalue=" + str(100 - itemdata[2])+ ",minvalue="+str(100 -itemdata[3])+"\n")
      except Exception as e:
           print(e,hostname)




if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 8)
    length = len(host)
    for i in range(length):
    	pool.apply_async(writefile,args=(i,))
    pool.close()
    pool.join()