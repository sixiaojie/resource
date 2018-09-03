from fluxdb import action
from orm import init

if __name__ == "__main__":
    init.init()
    action = action.Action()
    action.Threshold()
    action.biz_info()
    action.aggressive()
    action.Copy_table_common()
    action.D_value()
