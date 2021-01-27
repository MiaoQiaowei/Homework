from StockManager import *
import baostock as bs

if __name__ == '__main__':
    test = StockManager(["sh.600000"], "2019-12-01")
    a, b = test.CTA()
    dicts = dict.fromkeys(a, '买')
    dicts.update(dict.fromkeys(b, '卖'))
    dicts = sorted(dicts.items(), key=lambda t: t[0])
    print(dicts)