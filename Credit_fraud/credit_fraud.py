#!/usr/bin/env python
# coding: utf-8

# In[1]:


#使用逻辑回归对信用卡欺诈进行分类


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,precision_recall_curve
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


# In[3]:


#混淆矩阵可视化


# In[4]:


def plot_confusion_matrix(cm,classes,normalize=False,title='Confusion matrix',cmap=plt.cm.Blues):
    plt.figure()
    plt.imshow(cm,interpolation='nearest',cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks=np.arange(len(classes))
    plt.xticks(tick_marks,classes,rotation=0)
    plt.yticks(tick_marks,classes)
    
    thresh=cm.max()/2.
    for i ,j in itertools.product(range(cm.shape[0]),range(cm.shape[1])):
        plt.text(i,j,cm[i,j],
                horizontalalignment='center',
                color='white' if cm[i,j]>thresh else 'black')
        
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


# In[5]:


#显示模型评估结果


# In[6]:


def show_metrics():
    tp=cm[1,1]
    fn=cm[1,0]
    fp=cm[0,1]
    tn=cm[0,0]
    print('精确率:{:.3f}'.format(tp/(tp+fp)))
    print('召回率:{:.3f}'.format(tp/(tp+fn)))
    print('F1值:{:.3f}'.format(2*(((tp/(tp+fp))*(tp/(tp+fn)))/((tp/(tp+fp))+(tp/(tp+fn))))))


# In[7]:


#绘制精确率-召回率曲线


# In[8]:


def plot_precision_recall():
    plt.step(recall,precision,color='b',alpha=0.2,where='post')
    plt.fill_between(recall,precision,step='post',alpha=0.2,color='b')
    plt.plot(recall,precision,linewidth=2)
    plt.xlim([0.0,1])
    plt.ylim([0.0,1.05])
    plt.xlabel('召回率')
    plt.ylabel('精确率')
    plt.title('精确率-召回率 曲线')
    plt.show()


# In[9]:


#数据加载


# In[10]:


data=pd.read_csv('D:/kaggle/credit_fraud/creditcard.csv')


# In[11]:


data.describe()


# In[12]:


plt.rcParams['font.sans-serif']=['SimHei']


# In[13]:


plt.figure()


# In[14]:


ax=sns.countplot(x='Class',data=data)


# In[15]:


#显示交易笔数，欺诈交易笔数


# In[16]:


num=len(data)


# In[17]:


num_fraud=len(data[data['Class']==1])


# In[18]:


print('总交易笔数：',num)


# In[19]:


print('欺诈交易笔数：',num_fraud)


# In[20]:


print('诈骗交易比例:{:.6f}'.format(num_fraud/num))


# In[21]:


#欺诈和正常交易可视化


# In[22]:


f,(ax1,ax2)=plt.subplots(2,1,sharex=True,figsize=(15,8))
bins=50
ax1.hist(data.Time[data.Class==1],bins=bins,color='deeppink')
ax1.set_title('诈骗交易')
ax2.hist(data.Time[data.Class==0],bins=bins,color='deepskyblue')
ax2.set_title('正常交易')
plt.xlabel('时间')
plt.ylabel('交易次数')


# In[23]:


#对Amount进行数据规范化


# In[24]:


data['Amount_Norm']=StandardScaler().fit_transform(data['Amount'].values.reshape(-1,1))


# In[25]:


#特征选择


# In[26]:


y=np.array(data.Class.tolist())


# In[27]:


data=data.drop(['Time','Amount','Class'],axis=1)


# In[28]:


x=np.array(data.as_matrix())


# In[29]:


#准备训练集和测试集


# In[30]:


train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.1,random_state=33)


# In[31]:


#逻辑回归分类


# In[32]:


clf=LogisticRegression()


# In[33]:


clf.fit(train_x,train_y)


# In[34]:


predict_y=clf.predict(test_x)


# In[35]:


#预测样本的置信分数


# In[36]:


score_y=clf.decision_function(test_x)


# In[37]:


#计算混淆矩阵，并显示


# In[38]:


cm=confusion_matrix(test_y,predict_y)


# In[39]:


class_names=[0,1]


# In[40]:


#显示混淆矩阵


# In[41]:


plot_confusion_matrix(cm,classes=class_names,title='逻辑回归 混淆矩阵')


# In[42]:


plot_confusion_matrix(cm,classes=class_names,title='逻辑回归 混淆矩阵')


# In[43]:


show_metrics()


# In[44]:


#计算精确率，召回率，阈值用于可视化


# In[45]:


precision,recall,thresholds=precision_recall_curve(test_y,score_y)


# In[46]:


plot_precision_recall()


# In[ ]:




