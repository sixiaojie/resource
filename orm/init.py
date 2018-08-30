import time
from datetime import datetime,timedelta


from base.db import Mysql

current = str(time.strftime("%Y_%m",time.localtime(int(time.time()))))
last_month=str((datetime.now()-timedelta(days=30)).strftime("%Y_%m"))

sql1 = """
   CREATE TABLE  if NOT EXISTS  `threshold_%s` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `metric` varchar(20) NOT NULL,
  `hostname` varchar(20) NOT NULL,
  `groupname` varchar(20) NOT NULL,
  `minvalue` float NOT NULL,
  `hostnamecount` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
""" %current

sql2= """
    CREATE TABLE if NOT EXISTS `gthreshold_%s` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `metric` varchar(50) NOT NULL,
  `groupname` varchar(20) NOT NULL,
  `groupnamecount` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
""" %current

sql3= """
CREATE TABLE if NOT EXISTS `biz_info_%s` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(20) NOT NULL,
  `groupname` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
""" %current

sql4 = """
    CREATE TABLE if NOT EXISTS `groupnamecount_%s` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `groupname` varchar(20) NOT NULL,
  `count` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8
""" %current

sql5 = """
    create table if not exists `increment`(
    `groupname` varchar(20) NOT NULL,
    `count` int(5) DEFAULT NULL,    
    PRIMARY KEY (`groupname`)
    ) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8
"""


sql_list = [sql1,sql2,sql3,sql4,sql5]

db = Mysql()
for item in sql_list:
    db.write(item)