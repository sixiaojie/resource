# -*- coding:utf-8 -*-
import json
import requests
import sys
import MySQLdb
from base import common

from orm import init
init.init()
db = MySQLdb.connect(host='localhost',user='root',passwd='',db='test1')
db.set_character_set('utf8')
cur = db.cursor()

current = common.current
headers = {'Authorization':"Basic MDU4ZmQ1YWU5NTM1NDQyYmFkOTVlMTQzYmRkZjE3ODc6NGQyYzBjZGRhZWM4NDQ3ODgxNGQ4Yzk4MzMwNzQzOTc="}
f = open("host",'w+')
sub = {}
response = requests.get('http://127.0.0.1:10080/v1/biz/first',headers=headers).text
###这里将业务机器信息刷入到数据库
bind_info = {}
for project in json.loads(response)['data']:
	#print(project['id'],project['identity'])
	url='http://127.0.0.1:10080/v1/biz/first/'+str(project['id'])
	firstinfo = requests.get(url,headers=headers).text
	for secondinfo in json.loads(firstinfo)['data']['sub_biz']:
		#print(secondinfo["identity"],secondinfo["id"])
		url = 'http://127.0.0.1:10080/v1/biz/second/'+str(secondinfo['id'])
		second = requests.get(url,headers=headers).text
		for third in json.loads(second)['data']['sub_biz']:
			url = "http://127.0.0.1:10080/v1/biz/third/"+str(third["id"])+"/runtime"
			hostinfo = requests.get(url,headers=headers).text
			for hosts in json.loads(hostinfo)['data']:
				bind_info[hosts['privateIpAddress']] = True
				sql = "select * from biz_info_%s where ip='%s'" %(current,hosts['privateIpAddress'])
				cur.execute(sql)
				result = cur.fetchall()
				##这里通过ret确定是否执行insert操作
				ret = 0
				##这里将可执行的sql放入到list中
				sql_list = []
				##这里代表IP不存在，可以插入
				if len(result) != 1:
					ret = 1
				##这里代表ip 存在，但是属于未绑定机器，需要删除记录。重新插入
				elif result[0][0] == "" and result[0][2] == "":
					print(result)
					sql = "delete from biz_info_%s where ip='%s'" %(current,hosts['privateIpAddress'])
					sql_list.append(sql)
					ret = 1
				else:
					continue
				if ret == 1:
					sql = "insert into biz_info_%s values('%s','%s','%s','%s','%s','%s')" %(current,project['identity'],project['name'],secondinfo['identity'],secondinfo['name'],hosts['resourceName'],hosts['privateIpAddress'])
					sql_list.append(sql)
				for sql in sql_list:
					try:
						print(sql)
						cur.execute(sql)
						db.commit()
					except Exception as e:
						print(str(e))
						pass

url = "http://127.0.0.1:10080/v2/resource/runtime?fields[runtime]=resourceName,privateIpAddress&page[size]=0"
response = requests.get(url,headers=headers).text
###这里将未绑定信息更新到数据库
for item in json.loads(response)['data']:
	if bind_info.get(item["attributes"]["privateIpAddress"]) is None:
		sql = "insert into biz_info_%s values('%s','%s','%s','%s','%s','%s')" %(current,"","","","",item["attributes"]["resourceName"],item["attributes"]["privateIpAddress"])
		try:
			cur.execute(sql)
			db.commit()
		except Exception as e:
			print(str(e))
			pass

###这里不存在的机器从数据库中删除
for ip in bind_info:
	ret = 0
	for item in json.loads(response)['data']:
		if ip == item["attributes"]["privateIpAddress"]:
			ret = 1
			break
	if ret == 0:
		sql = "delete from biz_info_%s where ip='%s'" %(current,item["attributes"]["privateIpAddress"])
		try:
			cur.execute(sql)
			db.commit()
		except Exception as e:
			print(str(e))

