from fluxdb import action
from orm import init

if __name__ == "__main__":
    action = action.Action()
    action.cmdb_rsync_redis()
    action.Threshold()
    action.biz_info()
    action.increment()
    action.aggressive()
    action.Copy_table_common()
    action.D_value()
