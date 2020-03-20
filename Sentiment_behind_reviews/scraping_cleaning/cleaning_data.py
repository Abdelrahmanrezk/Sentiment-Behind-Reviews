#!/usr/bin/env python
# coding: utf-8

# # Cleaning scraped reviews
# 
# **Welcome to second stage of cleaning scraped reviews, what in this notebook:**
# - Get all reviews from mongo database
# - pipline process
#     - one for Arabic reviews
#     
# **Pipline process Structure**
# - Convert all reviews to lower case # for English Reviews
# - remove punctuations of all reviews
# - remove stop words # I found its so bad to remove stop words because its convert the meaning of the sentense at all but I have Designed my own stopwords for this project because of sentment analysis issues
# - spell correction
# - Tokenization
# - Steaming
# - Lemmatization
# - Frequency of Words

# ### loading packages we need

# In[1]:


from souq_configs import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import pymongo
from time import sleep
import pandas as pd
import numpy as np
import re
import csv
import sys
import logging
import logging.config
import nltk
from nltk.corpus import stopwords, webtext
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk.stem.isri import ISRIStemmer
from nltk.stem import WordNetLemmatizer 
from textblob import Word, TextBlob
from autocorrect import spell
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import unidecode
import string
import spacy
import unidecode
from word2number import w2n
from nlppreprocess import NLP
from tashaphyne.stemming import ArabicLightStemmer


# ### Connect to mongo cloud database

# In[2]:


client = pymongo.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_url}")
db = client.SBR


# ### Get all prodcuts in our cloud database

# In[3]:


products = list(db.products.find({}))


# In[4]:


print("Our scraped now are " + str(len(products)) + " Product")


# In[5]:


print("one product Data\n\n", products[1])


# ## Extract Reviews
# Our data now have all of products info not just reviews, so we need to get these reviews beside of this we need to separate Arabic and English reviews.
# 
# returned products are list each of them is document(objects as key value)
# 
# ### Function structure
# - First loop over all products
# - for each product get all reviews
# - for each review check its language
# 

# In[6]:


def export_all_reviews(products):
    '''
    Argument:
        list of products each of them as object with key and value
    return:
        from this products we just need the reviews so
        Arabic Reviews
        English Reviews
    '''
    all_arabic_reviews = []
    all_english_reviews = []
# Loop over products
    for indx,pro_val in enumerate(products):
# Loop over reviews
        for review in pro_val['product_reviews']:
            try:
                char_check = review[0]
                if char_check >= 'a' and char_check <= 'z' or char_check >= 'A' and char_check <= 'Z':
                    all_english_reviews.append(review)
                else:
                    all_arabic_reviews.append(review)
            except Exception as e:
# send exception to log folder
                logf = open("../logs_files/cleaning_reviews_error.log", "a+")
                logf.write("This error related to function export_all_reviews of cleaning_data file\n" 
                   + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines
    return all_arabic_reviews, all_english_reviews


# ### Prepare my own stopwords list
# I have designed these stopwords from multiple resource based on this problem of sentiment analysis

# In[7]:


def convert_file_of_stop_words_to_list(file_dir):
    '''
    Argument:
        file with stop words
    return:
        list of these stop words
    '''
    stop_words_designed = []
    with open(file_dir, 'r') as file:
        file = file.readlines()
        file = "".join(file)
        file = re.sub('[\[\]\'\",]', '', file)
        stop_words_designed = file.split()
    return stop_words_designed
    


# In[12]:


# file_dir = !pwd
# file_dir = file_dir[0]
# print(file_dir)
file_dir1 =  '../stop_words/nltk_stop_words_handle.txt'
file_di2 = '../stop_words/stop_list1.txt'
file_di3 ='../stop_words/updated_stop_words.txt'
stop_words_designed = convert_file_of_stop_words_to_list(file_dir1)
print("First File\n",len(stop_words_designed))
stop_words_designed.extend(convert_file_of_stop_words_to_list(file_di2))
print("\nAfter Expanding two file together\n",len(stop_words_designed))
# now remove dublicated via set
stop_words_designed = set(stop_words_designed)
stop_words_designed = list(stop_words_designed)
print("\nRemove Dublicated words\n",len(stop_words_designed))
arabic_stop_words_designed = convert_file_of_stop_words_to_list(file_di3)
print("\nUpdate the end file manually to remove some of words\n",len(arabic_stop_words_designed))


# In[13]:


all_arabic_reviews, all_english_reviews = export_all_reviews(products)


# In[14]:


print("Total Arabic reviews\n", len(all_arabic_reviews))
print("\nTotal English reviews\n", len(all_english_reviews))
print("\nSome of  Arabic reviews\n", all_arabic_reviews[:5])
print("\nsome of English reviews\n", all_english_reviews[:5])


# ### remove dublicate entry first
# use set features of python which return all of unique reviews
# then return as list

# In[15]:


all_arabic_reviews = set(all_arabic_reviews)
all_english_reviews = set(all_english_reviews)
all_arabic_reviews = list(all_arabic_reviews)
all_english_reviews = list(all_english_reviews)
print("Now Total Arabic reviews\n", len(all_arabic_reviews))
print("\nNow Total English reviews\n", len(all_english_reviews))


# #### keep only reviews more than one words because maybe work like قليلة has no meaning but  جودة قليلة

# In[16]:


def keep_those_reviews_greater_1_word(text_list):
    '''
    Argument:
        list of reviews
    return:
        list of reviews each of them grater than or equal 2 words
    '''
    updated_reviews = []
    for review in text_list:
        if len(review.split()) >= 2:
            updated_reviews.append(review)
            
    return updated_reviews


# In[17]:


all_arabic_reviews = keep_those_reviews_greater_1_word(all_arabic_reviews)
all_english_reviews = keep_those_reviews_greater_1_word(all_english_reviews)
print("Now Total Arabic reviews\n", len(all_arabic_reviews))
print("\nNow Total English reviews\n", len(all_english_reviews))


# In[18]:


def convert_list_of_strings_to_list_of_words(text):
    '''
    A function used to convert list of strings to be list of all words of these strings like:
    ['تليفون جيد',
 'ايباد ميني فور من افضل الايبادات في السوق وسعره كان مغري',]
    return:
        list of all words in all string like:
        ['تليفون', 'جيد'] and so on
    '''
    word_list = []
    for i in text:
        i = i.split()
        word_list.extend(i)
    return word_list


# In[19]:


def one_string_lower_conversation(sentence):
    '''
    Argument:
        text as string of words
    return:
        lower of this string
    '''
    return sentence.lower()
        


# In[20]:


def all_string_lower_conversation(text_list):
    '''
    Argument:
        list of strings and each of these strings does contain some of words
    return:
        lower each string in this list
    '''
    text_list = [one_string_lower_conversation(sentence) for sentence in text_list]
    return text_list


# **remove some of special characters characters**
# 
# like: َ"  ُ  ْ  "
# 

# In[21]:


def one_string_remove_diacritics(sentence):
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    sentence = re.sub(noise, '', sentence)
    return sentence


# In[22]:


def all_string_remove_diacritics(text_list):
    '''
    Argument:
        list of strings
    return:
        list of string without special chars from Arabic language
    '''
    text_list = [one_string_remove_diacritics(sentence) for sentence in text_list]
    return text_list


# **remove some of puncatution and repeated words**
# 
# like: $%&'()*+,-

# In[23]:


def one_string_remove_punctuation(sentence):
    '''
    Argument:
        string of words
    reutrn:
        string without punctuation like [.!?] and others
    '''
    sentence = sentence.split(' ')
    strs = ''
    punctuations = string.punctuation
    for word in sentence:
#         word = re.sub(r'(.)\1+', r'\1', word) # remove repated chars
        word = re.sub('[^\w\s+]',' ',word)
        if len(word) > 1 and not (word[0] >= 'a' and word[0] < 'z' or word[0] >= 'A' and word[0] < 'Z'):
            strs += word + ' '
    translator = str.maketrans('', '', punctuations)
    strs.translate(translator)
    return strs


# In[24]:


def all_strings_remove_punctuation(text_list):
    '''
    Argument:
        list of strings 
    reutrn:
        list of strings without punctuation like [.!?] and others
    '''
    text_list = [one_string_remove_punctuation(sentence) for sentence in text_list]
    return text_list


# In[25]:


def one_string_normalize_arabic(sentence):
    '''
    Argument:
        string of words
    return:
        string of words but standardize the words
    '''
    sentence = re.sub("[إأآا]", "ا", sentence)
    sentence = re.sub("ى", "ي", sentence)
    sentence = re.sub("ؤ", "ء", sentence)
    sentence = re.sub("ئ", "ء", sentence)
    sentence = re.sub("ة", "ه", sentence)
    sentence = re.sub("گ", "ك", sentence)
    return sentence


# In[26]:


def all_string_normalize_arabic(text_list):
    '''
    Argument:
        list of strings
    return:
        list of strings but replace some of chars  like ة to ه Arabic words
    '''
    text_list = [one_string_normalize_arabic(sentence) for sentence in text_list]
    return text_list


# In[27]:


def one_string_tokenization(sentence):
    '''
    Argument:
        String of words
    return:
        list of words
    '''
    sentence = word_tokenize(sentence)
    return sentence


# In[28]:


def all_string_tokenization(text_list):
    '''
    Argument:
        list of Strings
    return:
        list of strings and every string is list of words
    '''
    text_list = [one_string_tokenization(sentence) for sentence in text_list]
    return text_list


# In[29]:


def one_string_un_tokenization(sentence):
    '''
    Argument:
        list of words
    return:
        string of words
    '''
    sentence = " ".join(sentence)
    return sentence
    


# In[30]:


def all_string_un_tokenization(text_list):
    '''
    Argument:
        list of words
    return:
        string of words
    '''
    text_list = [one_string_un_tokenization(sentence) for sentence in text_list]
    return text_list
    


# In[31]:


def one_string_spelling_correction(sentence):
    '''
    Argument:
        string of words
    return:
        string of correct words
    '''
    
    sentence = str(TextBlob(sentence).correct())
    return sentence


# In[32]:


def all_string_spelling_correction(text_list):
    '''
    Argument:
        list of strings each of them are some of words
    return:
        list of correct strings
    '''
    text_list = [one_string_spelling_correction(sentence) for sentence in text_list]
    return text_list


# In[33]:


def one_string_steming(sentence, language):
    '''
    Argument:
        String of words
    return:
        list of words with steming which the root of the word
    '''
    sentence = one_string_tokenization(sentence)
    if language == 'English':
        stemmer = PorterStemmer()
        sentence = [stemmer.stem(word) for word in sentence]
    elif language == 'Arabic':
        stemmer = ISRIStemmer()
        sentence = [stemmer.stem(word) for word in sentence]
    return sentence


# In[34]:


def all_string_steming(text_list, language):
    '''
    Argument:
        list of strings
    return:
        list of strings with steming which the root of the word in each string
    '''
    text_list = [one_string_steming(sentence, language) for sentence in text_list]
    return text_list


# In[35]:


def one_string_Lemmatizing(sentence, language):
    '''
    Argument:
        String of words
    return:
        list of words with Lemmatizing
    '''
    sentence = one_string_tokenization(sentence)
    if language == 'English':
        lemmatizer = WordNetLemmatizer()
        sentence = [lemmatizer.lemmatize(word) for word in sentence]
    elif language == 'Arabic':
        stemmer = ArabicLightStemmer()
        sentence = [stemmer.light_stem(word) for word in sentence]
    return sentence


# In[36]:


def all_string_Lemmatizing(text_list, language):
    '''
    Argument:
        list of strings
    return:
        list of strings with steming which the root of the word in each string
    '''
    text_list = [one_string_Lemmatizing(sentence, language) for sentence in text_list]
    return text_list


# In[37]:


def one_string_stop_words(sentence, language):
    '''
    Argument:
        string of words
    return:
        remove stop words from this string like this, did
        but other words like not, no dont remove
    '''
    if language == 'English' or language == 'english':
        stop_words = NLP().stopword_list # retrive stopwords list
        sentence = sentence.split(' ')
        updated_sentence = ''
        for word in sentence:
            if word not in stop_words:
                updated_sentence += word + ' '
    
    elif language == 'Arabic' or language == 'arabic':
        stop_words = arabic_stop_words_designed 
        sentence = sentence.split(' ')
        updated_sentence = ''
        for word in sentence:
            if word not in stop_words:
                updated_sentence += word + ' '
    return updated_sentence
            


# In[38]:


def all_string_stop_words(text_list, language):
    '''
    Argument:
        list of string
    return:
        list of string without stop words
    '''
#     if language == 'English' or language == 'english':
#         stop_words = NLP().stopword_list()
        
    text_list = [one_string_stop_words(sentence, language) for sentence in text_list]
    return text_list


# In[39]:


def one_list_all_words(text_list):
    '''
    Argument:
        list of lists each of them are words
    return:
        one list contain all words
    '''
    updated_list = []
    [updated_list.extend(li) for li in text_list]
    return updated_list


# In[40]:


def arabic_pip_line(text_list):
    text_list = all_string_remove_diacritics(text_list)
    text_list = all_strings_remove_punctuation(text_list)
    text_list = all_string_normalize_arabic(text_list)
#     text_list = all_string_Lemmatizing(text_list, 'Arabic')
#     text_list = all_string_un_tokenization(text_list)
    text_list = all_string_stop_words(text_list, 'Arabic')
    return text_list
    


# In[ ]:




