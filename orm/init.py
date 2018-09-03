import time
from base import common


from base.db import Mysql


current = common.current
last_month=common.last_month

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

sql6 = """
    create table if not exists `host_aggres_%s`(
      `id` int not null auto_increment,
      `hostname` VARCHAR(20) NOT NULL,
      `avg_value` FLOAT(10) not NULL,
      `max_value` FLOAT(10) not null,
      `min_value` FLOAT(10) not NULL,
      `current` VARCHAR(15) not null,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
""" %current

sql7 = """
    create table if not exists `group_aggres_%s`(
      `id` int not null auto_increment,
      `hostname` VARCHAR(20) NOT NULL,
      `avg_value` FLOAT(10) not NULL,
      `max_value` FLOAT(10) not null,
      `min_value` FLOAT(10) not NULL,
      `current` VARCHAR(15) not null,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
""" %current

sql8 = """
    create table D_value(
	`id` int(5) not null auto_increment,
	`hostname` varchar(20) not null,
	`current` varchar(20) not null,
	`value` float not null,
	 PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""


def init():
    sql_list = [sql1,sql2,sql3,sql4,sql5,sql6,sql7,sql8]
    db = Mysql()
    for item in sql_list:
        db.write(item)

