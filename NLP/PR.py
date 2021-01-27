import numpy as np

omega_1 = np.array([[0,0,0],[1,0,0],[1,0,1],[1,1,0]]).T
omega_2 = np.array([[0,0,1],[0,1,0],[0,1,1],[1,1,1]]).T

#  将Omega_1和Omega_2两种模式作为一个整体考虑
x = np.concatenate((omega_1,omega_2),axis = 1)
#  求取均值(写作业要用到)
m = np.mean(x,axis = 1)
#  求取协方差矩阵
C = np.cov(x,bias=True)
#  求取协方差矩阵的特征值、特征向量
lamda,phi = np.linalg.eig(C)
#  对特征值从大到小排序
sort_lamda = -np.sort(-lamda)
#  从大到小排序，输出原始序列的索引
sort_index = np.argsort(-lamda)

#  降到2维，从大到小选取前2个特征向量
Selected_phi2 = np.concatenate((phi[:,sort_index[0]].reshape(3,1),
                               phi[:,sort_index[1]].reshape(3,1)),axis=1)
omega_1_tra2 = np.dot(Selected_phi2.T,omega_1)
omega_2_tra2 = np.dot(Selected_phi2.T,omega_2)
print('omega_1_tra2:',omega_1_tra2)
print('omega_2_tra2:',omega_2_tra2)
#  降到1维，从大到小选取前1个特征向量
Selected_phi1 = phi[:,sort_index[0]].reshape(3,1)
omega_1_tra1 = np.dot(Selected_phi1.T,omega_1)
omega_2_tra1 = np.dot(Selected_phi1.T,omega_2)
print('omega_1_tra1:',omega_1_tra1)
print('omega_2_tra1:',omega_2_tra1)