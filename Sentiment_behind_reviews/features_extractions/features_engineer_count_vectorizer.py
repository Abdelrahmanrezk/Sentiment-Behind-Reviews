#!/usr/bin/env python
# coding: utf-8

# # CountVectorizer

# ###  Text data requires special preparation before you can start using it for predictive modeling
# 
# We cannot work with text directly when using machine learning algorithms.
# 
# #### Instead, we need to convert the text to numbers.
# CountVectorizer use Bag of Words technolgy which depends  throws away all of the order information in the words and focuses on the occurrence of words in a document.

# In[1]:


import os
import sys
import pymongo
from time import sleep
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# splitting data
from sklearn.model_selection import train_test_split

# Features Extraction
from sklearn.feature_extraction.text import CountVectorizer

# Evaluation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

# models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC


# In[2]:


# import cleaning data file because of using some of its function of we need


# In[3]:


sys.path.append(os.path.abspath('../scraping_cleaning'))
from cleaning_data import *


# ## Read our classified file

# In[4]:


df_file = pd.read_csv('../csv_files/file_classified_reviews_updated.csv')
df_file.head()


# In[5]:


print("The number of reviews in our data set is: ", len(df_file))


# **Shuffle the data**

# In[6]:


df_file = df_file.sample(frac=1).reset_index(drop=True)


# In[7]:


# now 
df_file.head()


# ## split the data to train and testing 

# In[8]:


X = df_file['Arabic Reviews'] 
y = df_file['polarity']


# In[9]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1)
X_train[:5]


# In[10]:


print("Our training data now are: " + str(len(X_train))  + " Reviews")
print("Our testing data now are: " + str(len(X_test))  + " Reviews")
print("Our training data now are: " + str(len(y_train))  + " labels")
print("Our testing data now are: " + str(len(y_test))  + " labels")


# ### Take object from CountVectorizer & fit the data
# The CountVectorizer provides a simple way to both tokenize a **collection of text documents** like:
# ![example of data](../images/data_exaple_vectorize.png)
# 
# 
# and build a vocabulary of known words, but also to encode new documents using that vocabulary like:
# 
# ![example of output](../images/output_vectoriz.png)

# In[11]:


def count_vectorize(df):
    '''
    Argumen:
        df dataframe of multiple reviews
    return:
        Train & test arrays that can fir to the model
    '''
# I fit the vector to all of the data
    vectorizer = CountVectorizer()
    vectorize = vectorizer.fit(X) 
# fit splited data
    testing_data = vectorizer.transform(X_test)
    training_data = vectorizer.transform(X_train) 
# convert to array that can apply to ML model
    training_data = training_data.toarray()
    testing_data = testing_data.toarray()
    return training_data, testing_data


# In[12]:


training_data, testing_data = count_vectorize(X)


# ## result MultinomialNB Model

# In[13]:


clf_MultinomialNB = MultinomialNB()


# In[14]:


model = clf_MultinomialNB.fit(training_data, y_train)


# In[15]:


predict = model.predict(training_data)


# In[16]:


print("F1 score of our training data is: ", f1_score(y_train, predict, average='micro'))


# In[17]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[18]:


predict = model.predict(testing_data)


# In[19]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[20]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_test, predict))


# ## result using LogisticRegression Model

# In[21]:


clf_LogisticRegression = LogisticRegression(penalty='l2', tol=0.00001, solver='liblinear',max_iter=1000)


# In[22]:


logistic_model = clf_LogisticRegression.fit(training_data, y_train)


# In[23]:


predict = logistic_model.predict(training_data)


# In[24]:


print("F1 score of our testing data is: ", f1_score(y_train, predict, average='micro'))


# In[25]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[26]:


predict = logistic_model.predict(testing_data)


# In[27]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[28]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_test, predict))


# ### result using SVC Model

# In[29]:


clf_SVC = SVC(kernel='linear')


# In[30]:


svc_model = clf_SVC.fit(training_data, y_train)


# In[31]:


predict = svc_model.predict(training_data)


# In[32]:


print("F1 score of our testing data is: ", f1_score(y_train, predict, average='micro'))


# In[33]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[34]:


predict = svc_model.predict(testing_data)


# In[35]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[36]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_test, predict))


# In[ ]:




