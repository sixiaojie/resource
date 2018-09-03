from datetime import datetime,timedelta
import time
current = str(time.strftime("%Y_%m",time.localtime(int(time.time()))))
last_month=str((datetime.now()-timedelta(days=30)).strftime("%Y_%m"))
current_month_influxdb=str((datetime.now()-timedelta(days=30)).strftime("%Y-%m"))