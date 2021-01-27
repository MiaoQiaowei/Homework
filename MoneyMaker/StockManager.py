import baostock as bs
import pandas as pd
import numpy as np
import seaborn as sns
import tushare as ts
from datetime import datetime, date, timedelta

class StockManager:

    def __init__(self,bench_mark="sh.000300"):
        self.bench_mark = self.loadDate([bench_mark])

    def update(self,codes,
                 start_date = str((date.today()+timedelta(-300)).strftime("%Y-%m-%d")),
                 end_date=str(date.today().strftime("%Y-%m-%d"))):
        '''
        更新数据
        :param codes: 查询代码list
        :param start_date: 开始日期 str "年年-月月-日日"
        :param end_date: 结束日期 str "年年-月月-日日"
        :return: data
        '''
        self.data = self.loadDate(codes,start_date,end_date)
        self.codes = codes

    def loadDate(self,codes,
                 start_date = str((date.today()+timedelta(-300)).strftime("%Y-%m-%d")),
                 end_date=str(date.today().strftime("%Y-%m-%d"))):
        '''
        加载数据
        :param codes: 查询代码list
        :param start_date: 开始日期 str "年年-月月-日日"
        :param end_date: 结束日期 str "年年-月月-日日"
        :return: data
        '''
        bs.login()
        data = {}
        for code in codes:
            res = bs.query_history_k_data_plus(code, "date,open,high,low,close",
                                               start_date=start_date, end_date=end_date,
                                               frequency="d", adjustflag="3")
            assert res.error_code == '0'
            data[code] = []
            while res.next():
                data[code].append(res.get_row_data())
            data[code] = pd.DataFrame(data[code], columns=res.fields).set_index('date')

        print("数据加载完毕！")
        bs.logout()
        return data

    def CTA(self,low=5,high=30):
        '''
        CTA:
        双均线策略
        短线上穿长线买入：金叉
        短线下穿长线卖出：死叉
        :param low: 低线[5,10]
        :param high: 中线[30,60],高线[120,240]
        :return:
        '''
        golden_cross = []
        death_cross = []


        for code in self.codes:
            data = self.data[code]
            low_list = data['open'].rolling(low).mean()
            high_list = data['open'].rolling(high).mean()

            low_str = 'ma'+str(low)
            high_str = 'ma'+str(high)
            data[low_str] = low_list
            data[high_str] = high_list
            data.dropna()

            s_a = data[low_str] < data[high_str]
            s_b = data[low_str] >= data[high_str]

            golden_cross = data[s_a & s_b.shift(1)].index
            death_cross = data[~(s_a | s_b.shift(1))].index
            golden_cross = [i for i in golden_cross]
            death_cross = [i for i in death_cross]
            self.data[code] = data

        return golden_cross,death_cross

    def computeROE(self,code, year, quarter):
        '''
        计算ROM指数，15%-25%区间为好
        :param year:年
        :param quarter:季度
        :return:值
        '''
        # 查询杜邦指数
        dupont_list = []
        rs_dupont = bs.query_dupont_data(code, year, quarter)
        while (rs_dupont.error_code == '0') & rs_dupont.next():
            dupont_list.append(rs_dupont.get_row_data())
        result_profit = pd.DataFrame(dupont_list,columns=rs_dupont.fields)

        return result_profit

    def MFS(self):
        '''
        多因子选股
        :return:股票代码
        '''
        bs.login()
        rs = bs.query_stock_basic()

        result_profit = pd.DataFrame()
        while (rs.error_code == '0') & rs.next():  # 获取一条记录，将记录合并在一起
            code = rs.get_row_data()[0]
            for year in range(2019, 2020):
                df = self.computeROE(code, year, 4)
                if df.empty:
                    continue
                else:
                    if result_profit.empty:
                        result_profit = df
                    else:
                        result_profit = result_profit.append(df)

        print(result_profit)
        result = result_profit[['code', 'dupontROE']]
        result = result[result['dupontROE'] != '']
        result['dupontROE'] = result['dupontROE'].astype(float)
        sr_mean = result.groupby(by=['code'])['dupontROE'].mean()
        sr_std = result.groupby(by=['code'])['dupontROE'].std()

        df = pd.DataFrame({'mean': sr_mean.data, 'std':sr_std.data},columns=['mean', 'std'], index=sr_mean.index)
        df.dropna()
        df = df.sort_values(['mean', 'std'], ascending=[False, True])
        result = df[:10]
        print(result)
        bs.logout()
        return result

    def buy(self,code='000002.XSHG',cash = 0):


        return 1

    def sell(self,code,rate):
        return 1

    def sittings(self):
        return 1


if __name__ == '__main__':
    test = StockManager()
    # test.update(["sh.600000"],"2019-12-01")
    # print(test.codes)
    # print(test.data)
    # a,b = test.CTA()
    # dicts = dict.fromkeys(a,'买')
    # dicts.update(dict.fromkeys(b,'卖'))
    # dicts = sorted(dicts.items(),key= lambda t:t[0])
    # print(dicts)
    # print(test.bench_mark)
    test.MFS()