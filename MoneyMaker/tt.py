import baostock as bs
import pandas as pd
def computeROE(code, year, quarter):
# 查询杜邦指数
    dupont_list = []
    rs_dupont = bs.query_dupont_data(code, year, quarter)
    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list,columns=rs_dupont.fields)
    # 打印输出
    return result_profit

def compute_total_ROE():
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond error_msg:' + lg.error_msg)
    # 获取全部证券基本资料
    rs = bs.query_stock_basic()
    # rs = bs.query_stock_basic(code_name="浦发银行") # 支持模糊查询
    print('query_stock_basic respond error_code:' + rs.error_code)
    print('query_stock_basic respond error_msg:' + rs.error_msg)
    result_profit = pd.DataFrame()
    while (rs.error_code == '0') & rs.next(): # 获取一条记录，将记录合并在一起
        code = rs.get_row_data()[0]
        for year in range(2017, 2018):
            df = computeROE(code, year, 4)
            if df.empty:
                continue
            else:
                if result_profit.empty:
                    result_profit = df
                else:
                    result_profit = result_profit.append(df)
    # 原始数据存储
    result_profit.to_csv("dupont_data_row.csv",encoding="gbk", index=False)
    # 筛选有用数据
    result = result_profit[['code', 'dupontROE']]
    result = result[result['dupontROE'] != '']
    result['dupontROE'] = result['dupontROE'].astype(float)
    series_mean = result.groupby(by=['code'])['dupontROE'].mean()
    series_std = result.groupby(by=['code'])['dupontROE'].std()
    df2 = pd.DataFrame({'mean': series_mean.data, 'std': series_std.data}, columns=['mean', 'std'], index=series_mean.index)
    df2 = df2.sort_values(['mean'])
    df2.to_csv("dupont_data_sorted_by_roe.csv", encoding="gbk", index=True)
# 登出系统 bs.logout()
if __name__ == '__main__':
    compute_total_ROE()