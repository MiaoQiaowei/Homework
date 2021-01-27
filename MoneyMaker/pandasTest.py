import baostock as bs
import pandas as pd
import numpy as np
import seaborn as sns
import tushare as ts
from datetime import datetime, date, timedelta


class

def getData(code):
    df = pd.read_csv('600519.csv',index_col='date',parse_dates=['date'])[['open','close','low','high']]
    l = len(df)
    #选5日均线和60日均线
    return df[l-300:]


def CTA(data,low,high,check=False):
    # 双均线策略（什么时候买入，什么时候卖出）
    '''
    双均线策略
    :param data: 单支基金历史数据
    :param low: 短线均值[5,10]
    :param high: 中线均值[30,60],长线均值[120,240]
    :param check: 是否查询今天操作
    :return: 金叉，死叉
    '''
    high_str = 'ma'+ str(high)
    low_str = 'ma' + str(low)
    data[high_str] = data['open'].rolling(high).mean()
    data[low_str] = data['open'].rolling(low).mean()
    data.dropna()

    se_1 = data[low_str] < data[high_str]
    se_2 = data[low_str] >= data[high_str]


    golden_cross = data[se_1 & se_2.shift(1)].index
    death_cross = data[~(se_1 | se_2.shift(1))].index
    golden_cross = [i.to_pydatetime().strftime("%Y-%m-%d") for i in golden_cross]
    death_cross = [i.to_pydatetime().strftime("%Y-%m-%d") for i in death_cross]


    if check:
        day = date.today()
        day_of_week = datetime.now().weekday()
        delta = -max(0,day_of_week-4)
        print("今天是",day)
        day +=  timedelta(4)
        day = day.strftime("%Y-%m-%d")
        if day in golden_cross:
            print(day+"买入")
        elif day in death_cross:
            print(day+"卖出")
        else:
            print("维持现状")

    return  golden_cross, death_cross




def test(data,money,in_or_out):





if __name__ == '__main__':
    bs.login()
    #双均线策略测试
    data = getData()
    golden_cross,death_cross = CTA(data,5,30,True)
    get_money = test()

    bs.logout()
