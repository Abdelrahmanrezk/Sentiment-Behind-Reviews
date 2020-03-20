#!/usr/bin/env python
# coding: utf-8

# # One Hot Encoding

# one hot encoding is used to encode categorical data and working as follow:
# for each catecorial or word of data convert to integer number but binarry classifcation and each word is 0 or 1.
# 
# Then, each integer value is represented as a binary vector that is all zero values except the index of the integer, which is marked with a 1.
# also one hot encoding encode in such away:
# - words represent each words even those which are repeated
# - but columns represent unique words of our corps
# 
# ### one hot is used for categorical data like colors = 'red', 'green'

# In[1]:


from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import itertools
import sys
import os
sys.path.append(os.path.abspath('../scraping_cleaning'))
from cleaning_data import *


# ### Example of one hot encoding without library "Manual One Hot Encoding"
# 
# Function below take an argument as string like "I am learning NLP"
# and return one hot encoding example like:
# 
# ![one_hot_encoding](../images/one_hot_encoding.png "one_hot_encoding")
# 

# In[2]:


def convert_string_to_one_hot_manual(text):
    '''
    Argument:
        text as string
    return:
        one hot encoding data frame
    '''
    one_hot_encoding = []
    text_list = text.split() # covert string to list
# make each word as key and integer as value
    text_words_as_key = dict((c,i) for i,c in enumerate(text_list))
    for key,val in enumerate(text_list):
        
# list of zeros and for each word will assign one and everyone else 0
        words = [0 for i in text_list]
    
# assign one for the word in our dictionary
        words[text_words_as_key[val]] = 1
    
# append this one_hot_word vector
        one_hot_encoding.append(words)
    
    one_hot_encoding = pd.DataFrame(one_hot_encoding, columns=text_list)
    return one_hot_encoding


# In[3]:


def convert_string_to_one_hot_using_pannds(text):
    '''
    Argument:
        text as string
    return:
        apply one hot encoding on text
    '''
    text_list = text.split() # covert string to list
    print(len(text_list))
    one_hot_encoding = pd.get_dummies(text_list) # using pandas
    
    return one_hot_encoding
    


# ## One-Hot Encoding using sklearn
# **To convert  one hot with sklearn you first convert to label encoding.**

# In[4]:


def convert_string_to_labelencoder_using_sklearn(text):
    '''
    Argument:
        function take list of strings:
        first convert these strings to list of all words of these string
        second apply sklearn to one-hot-encoding
     return: hot
    '''
# using function from data cleaning to convert the list of strings
    text = convert_list_of_strings_to_list_of_words(text)

# convert to data frame of pandas
    text = pd.DataFrame(text, columns=['reviews_words'])
# creating instance object from labelencoder
    labelencoder = LabelEncoder()
    text['labels_encode'] = labelencoder.fit_transform(text['reviews_words'])
    return text


# In[5]:


text = convert_string_to_labelencoder_using_sklearn(all_arabic_reviews)
text


# ### convert to one hot
# **function above convert first to label encoding then we convert to one hot encoding.**
# 
# Though label encoding is straight way but it has the disadvantage that the numeric values can be misinterpreted by algorithms as having some sort of hierarchy/order as above.
# 
# OneHotEncoder from SciKit library only takes numerical categorical values, hence any value of string type should be label encoded before one hot encoded. So taking the dataframe from the previous example, we will apply OneHotEncoder.

# In[6]:


def convert_string_to_one_hot_using_sklearn(text):
    '''
    Argument:
        dataframe from the previous example
    return:
        apply OneHotEncoder on column 
        
    '''
    one_hot_encod = OneHotEncoder()
    one_hot_encod = pd.DataFrame(one_hot_encod.fit_transform(text[['labels_encode']]).toarray(), dtype=int)
    return one_hot_encod


# In[7]:


one_hot_encod = convert_string_to_one_hot_using_sklearn(text[:10])
one_hot_encod


# In[ ]:





# In[ ]:




