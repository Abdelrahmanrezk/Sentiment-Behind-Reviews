import os
import re
import csv
import sys
import string
import pymongo
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords, webtext
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.isri import ISRIStemmer
from nltk.stem import WordNetLemmatizer 
from textblob import Word, TextBlob
from autocorrect import spell
from nlppreprocess import NLP
from tashaphyne.stemming import ArabicLightStemmer







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





def one_string_lower_conversation(sentence):
    '''
    Argument:
        text as string of words
    return:
        lower of this string
    '''
    return sentence.lower()
        




def all_string_lower_conversation(text_list):
    '''
    Argument:
        list of strings and each of these strings does contain some of words
    return:
        lower each string in this list
    '''
    text_list = [one_string_lower_conversation(sentence) for sentence in text_list]
    return text_list





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





def all_string_remove_diacritics(text_list):
    '''
    Argument:
        list of strings
    return:
        list of string without special chars from Arabic language
    '''
    text_list = [one_string_remove_diacritics(sentence) for sentence in text_list]
    return text_list



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




def all_strings_remove_punctuation(text_list):
    '''
    Argument:
        list of strings 
    reutrn:
        list of strings without punctuation like [.!?] and others
    '''
    text_list = [one_string_remove_punctuation(sentence) for sentence in text_list]
    return text_list




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




def all_string_normalize_arabic(text_list):
    '''
    Argument:
        list of strings
    return:
        list of strings but replace some of chars  like ة to ه Arabic words
    '''
    text_list = [one_string_normalize_arabic(sentence) for sentence in text_list]
    return text_list




def one_string_tokenization(sentence):
    '''
    Argument:
        String of words
    return:
        list of words
    '''
    sentence = word_tokenize(sentence)
    return sentence




def all_string_tokenization(text_list):
    '''
    Argument:
        list of Strings
    return:
        list of strings and every string is list of words
    '''
    text_list = [one_string_tokenization(sentence) for sentence in text_list]
    return text_list




def one_string_un_tokenization(sentence):
    '''
    Argument:
        list of words
    return:
        string of words
    '''
    sentence = " ".join(sentence)
    return sentence
    




def all_string_un_tokenization(text_list):
    '''
    Argument:
        list of words
    return:
        string of words
    '''
    text_list = [one_string_un_tokenization(sentence) for sentence in text_list]
    return text_list
    




def one_string_spelling_correction(sentence):
    '''
    Argument:
        string of words
    return:
        string of correct words
    '''
    
    sentence = str(TextBlob(sentence).correct())
    return sentence




def all_string_spelling_correction(text_list):
    '''
    Argument:
        list of strings each of them are some of words
    return:
        list of correct strings
    '''
    text_list = [one_string_spelling_correction(sentence) for sentence in text_list]
    return text_list




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




def all_string_steming(text_list, language):
    '''
    Argument:
        list of strings
    return:
        list of strings with steming which the root of the word in each string
    '''
    text_list = [one_string_steming(sentence, language) for sentence in text_list]
    return text_list




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




def all_string_Lemmatizing(text_list, language):
    '''
    Argument:
        list of strings
    return:
        list of strings with steming which the root of the word in each string
    '''
    text_list = [one_string_Lemmatizing(sentence, language) for sentence in text_list]
    return text_list







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

        file_dir1 =  'sentiment_behind_reviews/ml_work/stop_words/nltk_stop_words_handle.txt'
        file_di2 = 'sentiment_behind_reviews/ml_work/stop_words/stop_list1.txt'
        file_di3 ='sentiment_behind_reviews/ml_work/stop_words/updated_stop_words.txt'

        stop_words_designed = []
        stop_words_designed.extend(convert_file_of_stop_words_to_list(file_di2))
        
        stop_words_designed = set(stop_words_designed)
        stop_words_designed = list(stop_words_designed)
        arabic_stop_words_designed = convert_file_of_stop_words_to_list(file_di3)

        stop_words = arabic_stop_words_designed 
        sentence = sentence.split(' ')
        updated_sentence = ''
        for word in sentence:
            if word not in stop_words:
                updated_sentence += word + ' '
    return updated_sentence
            




def all_string_stop_words(text_list, language):
    '''
    Argument:
        list of string
    return:
        list of string without stop words
    '''        
    text_list = [one_string_stop_words(sentence, language) for sentence in text_list]
    return text_list




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



def arabic_pip_line(text_list):
    text_list = all_string_remove_diacritics(text_list)
    text_list = all_strings_remove_punctuation(text_list)
    text_list = all_string_normalize_arabic(text_list)
    text_list = all_string_stop_words(text_list, 'Arabic')

#     text_list = all_string_Lemmatizing(text_list, 'Arabic')
    return text_list
    


