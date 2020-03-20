#!/usr/bin/env python
# coding: utf-8

# # TfidfVectorizer

# **Word counts like CountVectorizer are a good starting point, but are very basic.**
# 
# One of the problem related to this is counts words like “the, and, or, there and others" will appear many times and their large counts will not be very meaningful in the encoded vectors and cause our model to missunderstand important words than those repeated many times.
# 
# Alternative way of this is to calculate word frequencies which the first of tfidf is tf--> Term Frequency, then  down scale these words that appear a lot across documents using the second part which is idf --> Inverse Document Frequency.
# 
# 

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
from sklearn.feature_extraction.text import TfidfVectorizer

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


# ### Take object from TfidfVectorizer & fit the data
# The CountVectorizer provides a simple way to both tokenize a **collection of text documents** like:
# ![example of data](../images/TfidfVectorizer_df_file.png)
# 
# 
# and build a vocabulary of known words, but also to encode new documents using that vocabulary like:
# ![example of output](../images/TfidfVectorizervocabulary_.png)
# 
# **The inverse document frequencies are calculated for each word in the vocabulary, assigning the lowest score of 1.0 to the most frequently observed word: "the".**

# In[11]:


def tfidf_vectorizer(df):
    '''
    Argumen:
        df dataframe of multiple reviews
    return:
        Train & test arrays that can fir to the model
    '''
# I fit the vector to all of the data
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer = tfidf_vectorizer.fit(X) 
    word_idf_weights = tfidf_vectorizer.idf_
    print("Our 10 words weights\n\n",word_idf_weights[:10])
# fit splited data
    testing_data = tfidf_vectorizer.transform(X_test)
    training_data = tfidf_vectorizer.transform(X_train) 
# convert to array that can apply to ML model
    training_data = training_data.toarray()
    testing_data = testing_data.toarray()
    return training_data, testing_data


# In[12]:


training_data, testing_data = tfidf_vectorizer(X)


# In[13]:


# first shape is the data itself and second shape is the BOW in our data
print("Our new vectorized data: " + str(training_data.shape))
print("Our new vectorized data: " + str(testing_data.shape)) 
print("The first 2 review after transform: \n", testing_data[:2])


# ### result using naive_bayes MultinomialNB Model

# In[14]:


clf_MultinomialNB = MultinomialNB()


# In[15]:


model = clf_MultinomialNB.fit(training_data, y_train)


# In[16]:


predict = model.predict(training_data)


# In[17]:


print("F1 score of our training data is: ", f1_score(y_train, predict, average='micro'))


# In[18]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[19]:


predict = model.predict(testing_data)


# In[20]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[21]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_test, predict))


# ### result using LogisticRegression Model

# In[22]:


clf_LogisticRegression = LogisticRegression(penalty='l2', tol=0.00001, solver='liblinear',max_iter=1000)


# In[23]:


logistic_model = clf_LogisticRegression.fit(training_data, y_train)


# In[24]:


predict = logistic_model.predict(training_data)


# In[25]:


print("F1 score of our testing data is: ", f1_score(y_train, predict, average='micro'))


# In[26]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[27]:


predict = logistic_model.predict(testing_data)


# In[28]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[29]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_test, predict))


# ### result using SVC Model

# In[30]:


clf_SVC = SVC(kernel='linear')


# In[31]:


svc_model = clf_SVC.fit(training_data, y_train)


# In[32]:


predict = svc_model.predict(training_data)


# In[33]:


print("F1 score of our testing data is: ", f1_score(y_train, predict, average='micro'))


# In[34]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[35]:


predict = svc_model.predict(testing_data)


# In[36]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[37]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_test, predict))


# In[38]:


clf_SVC = SVC(kernel='poly', degree=2)


# In[39]:


svc_model = clf_SVC.fit(training_data, y_train)


# In[40]:


predict = svc_model.predict(training_data)


# In[41]:


print("F1 score of our training data is: ", f1_score(y_train, predict, average='micro'))


# In[42]:


print("Evalution Matrix of training data is \n", confusion_matrix(y_train, predict))


# In[43]:


predict = svc_model.predict(testing_data)


# In[44]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[45]:


print("Evalution Matrix of testing data is \n", confusion_matrix(y_test, predict))


# In[46]:


clf_SVC = SVC(kernel='sigmoid')


# In[47]:


svc_model = clf_SVC.fit(training_data, y_train)


# In[48]:


predict = svc_model.predict(training_data)


# In[49]:


print("F1 score of our training data is: ", f1_score(y_train, predict, average='micro'))


# In[50]:


predict = svc_model.predict(testing_data)


# In[51]:


print("F1 score of our testing data is: ", f1_score(y_test, predict, average='micro'))


# In[52]:


print("Evalution Matrix of testing data is \n", confusion_matrix(y_test, predict))


# In[ ]:




