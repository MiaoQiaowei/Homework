import numpy as np
import re
import math

class HMM:
    
    def forward(self,A,B,pi,O):
        days = len(O)
        ans = []
        for day in range(days):
            index = O[day]
            if day == 0:
                ans = np.multiply(B[:,index],pi.T)
            else:
                tmp = np.zeros(3)
                for i in range(3):
                    tmp[i] = np.dot(ans,A[:,i])*B[i,index]
                ans = tmp
        return ans

    def backward(self,A,B,pi,O):
        days = len(O)
        weathers,types = B.shape
        ans = np.ones(weathers)
        for day in range(days):
            index = O[days-1-day]
            for i in range(weathers):
                if day!=0 :
                    tmp = np.multiply(A[i,:],B[:,index].T)
                else:
                    tmp = np.multiply(pi,B[:,index].T)
                tmp = np.dot(ans.T,tmp)
                ans = tmp
        return ans

def EM(l,p,q,x,times):
    def cal(l,p,q,xi):
        return (l*math.pow(p,xi) * math.pow(1-p,1-xi))/(l*math.pow(p,xi)*math.pow(1-p,1-xi)+(1-l)*math.pow(q,xi)*math.pow(1-q,1-xi))

    for i in range(times):
        tmp =[cal(l,p,q,t) for t in x ]
        l_ = np.mean(tmp)
        p_ = np.sum(np.multiply(tmp,x))/np.sum(tmp)
        tmp = [1-t for t in tmp]
        q_ = np.sum(np.multiply(tmp,x))/np.sum(tmp)
        l = l_
        q = q_
        p = p_
    return l,p,q


def count(str):
    dicts = {}
    for i in str:
        if "\u4e00" <= i <= "\u9fff":
            if i in dicts:
                dicts[i]+=1
            else:
                dicts[i] = 1
    return sorted(dicts.items, key= lambda t:t[1])




    
     
    

if __name__ == "__main__":
    hmm = HMM()
    pi = np.array([0.63,0.17,0.20])       #初始概率矩阵 
    A  = np.array([[0.5,0.375,0.125],
                   [0.25,0.125,0.625],
                   [0.25,0.375,0.375]])   #状态转移矩阵
    B  = np.array([[0.60,0.20,0.15,0.05],
                   [0.25,0.25,0.25,0.25],
                   [0.05,0.10,0.35,0.5]]) #发射概率矩阵 
    O  = np.array([0,2,3])                #观测矩阵 


    # hmm = HMM()
    # # ans = hmm.forward(A,B,pi,O)
    # # print(ans)
    # # ans = hmm.backward(A,B,pi,O)
    # # print(ans)

    # #EM算法
    # see = [1,1,1,1,1,1,0,0,0,0]
    # l,p,q = [0.5,0.5,0.5]
    # #a,lambda 正， 1-lambda 负
    # #b 正 p
    # #c 正 q
    # l,p,q = EM(l,p,q,see,100)
    # print(l,p,q)

    #单字字频统计
    # str = "输出：hello world, 你好世界, 世界你好，你好Python输入."
    # dict = {}
    # for i in str:
    #     print(i)
    #     if i >= u'u4e00' and i <= u'u9fa5':
    #         if i in dict:
    #             dict[i]+=1
    #         else:
    #             dict[i] = 1
    
    # result = sorted(dict.items(),key= lambda d:d[0])
    # print(result)

    #前向算法
    #二元语法模型
    #EM算法
    #匹配
    str = "输出：hello world, 你好世界, 世界你好，你好Python输入."
    result = count(str)
    print(str)


    
    