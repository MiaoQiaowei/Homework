import numpy as np
import math
import re
import operator

def EM_three():
    x = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1]
    l , p , q = 0.4,0.6,0.7
    times  = 100
    # x = np.array(x)

    for time in range(times):
        p_ = np.array([math.pow(p,i)*math.pow(1-p,1-i) for i in x])*l
        q_ = np.array([math.pow(q,i)*math.pow(1-q,1-i) for i in x])*(1-l)
        l_ = p_/(p_+q_)
        l = np.mean(l_)
        p = np.sum(np.multiply(l_,x))/np.sum(l_)
        q = np.sum(np.multiply(1-l_,x))/np.sum(1-l_)
    
    print(l,p,q)

class HMM:
    def __init__(self):
        self.A = np.array([ [0.5,0.375,0.125],
                            [0.25,0.125,0.625],
                            [0.25,0.375,0.375]])
        self.B = np.array([ [0.60,0.20,0.15,0.05],
                            [0.25,0.25,0.25,0.25],
                            [0.05,0.10,0.35,0.5]])
        self.pi= np.array([0.63,0.17,0.20])
        self.O = np.array([0,2,3])
    
    def forward(self):
        days = len(self.O)
        ans = np.zeros(3)
        tmp = np.zeros(3)
        for day in range(days):
            today = self.O[day]
            if day == 0:
                tmp = np.multiply(self.B[:,today],self.pi.T)
            else:
                tmp = np.array(
                    [np.sum(np.multiply(ans,self.A[:,i])) for i in range(3) ]
                )
                tmp = np.multiply(tmp,self.B[:,today])
            ans = tmp.copy()
            print(day,":",ans)
        return np.sum(ans)

    def backward(self):
        days = len(self.O)
        ans = np.zeros(3)
        tmp = np.ones(3)
        for day in reversed(range(days)):
            today = self.O[day]
            if day!=0:
                for i in range(3):
                    ans[i] = np.sum(tmp*self.A[i,:]*self.B[:,today])
            else:
                ans =tmp*self.pi*self.B[:,today]
            tmp = ans.copy()
            print(day,":",ans)
        return np.sum(ans)

    def viterbi(self):
        
        days = len(self.O)
        pre = np.zeros((3,days))
        ans = np.zeros(3)
        tmp = np.zeros(3)
        for day in range(days):
            today = self.O[day]
            if day == 0:
                tmp = self.pi*self.B[:,today]
                for i in range(3):
                    pre[i,0] = i
            else:
                for i in range(3):
                    arr = ans*self.A[:,i]
                    tmp[i] = max(arr)
                    pre[i,day] = np.argmax(arr)
                tmp = tmp*self.B[:,today]
            ans = tmp.copy()
            print(day,":",ans)
        result = []
        days -= 1
        nxt = 0
        while days>=0:
            if days == 2:
                index = np.argmax(ans)
                nxt = pre[index,days]
                result.append(index)
            else:
                result.append(nxt)
                nxt = pre[nxt,days]
            nxt = int(nxt)
            days-=1
        
        return reversed(result)

    def baum_welch(self):

        return 

def singleCount():
    str = "输出：hello world, 你好世界, 世界你好，你好Python输入."
    dicts = {}
    for i in str:
        if '\u4e00'<=i<='\u9f5a':
            if i not in dicts:
                dicts[i] = 1
            else:
                dicts[i]+=1
    ans = sorted(dicts.items(),key=lambda t: t[1],reverse=True)
    print(ans)

def pairCount():
    str = "发展中国家（Developing country）也称作开发中国家、欠发达国家，指经济、技术、人民生活水平程度较低的国家，与发达国家相对。"
    dicts = {}
    pre =""
    for i in str:
        if '\u4e00'<=i<='\u9f5a':
            if pre!="":
                inStr = pre+i
                if inStr not in dicts:
                    dicts[inStr] = 1
                else:
                    dicts[inStr] += 1
            pre = i
        else:
            pre = ""
    ans = sorted(dicts.items(),key=lambda t: t[1],reverse=True)
    print(ans)

def maxPari():
    str = '时间就是生命' 
    dicts = ['时间', '就', '是',  '生命']    
    maxlen = max([len(i) for i in dicts])
    start = 0
    out = ""
    while start!= len(str):
        substr = str[start:start+maxlen]
        while len(substr)!=1 :
            if substr in dicts:
                break
            else:
                substr = substr[:len(substr)-1]
        out+=substr+"/"
        start+=len(substr)
    print(out)




# hmm = HMM()
# print(hmm.forward())
# print(hmm.backward())
# print(hmm.viterbi())
singleCount()
# pairCount()
# maxPari()

