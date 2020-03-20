#!/usr/bin/env python
# coding: utf-8

# # Reviews Handling
# based on the problems of Sentimen Classifcation some of reviews file have muliple columns like:
# - 'reviews.dateAdded' 
# - 'reviews.dateSeen'
# - others columns
# 
# but we just interset in two columns the text review and the rate of each review.
# 
# So here is a function that handle these problems and return the reviews with two columns.
# 
# **Another Function to compine the returned data frames to one data frame:**
# combine_positive_negative_reviews this function is to handle returned data frame as just one data frame with the two columns
# 
# **Another Function to shuffle the reviews of the returned combined data frame**
# 
# **Another Function to convert the data frame to csv file**

# In[1]:


import pandas as pd
import os
import datetime


# ## Reviews_handling function
# 
# A function below handle files that contain multiple of columns but we need the reviews and the rate of each reviews, but based on rate we return that all of reviews > 3 is positive other wise is negative which <= 3.

# In[2]:


def reviews_handling(data_frame, review_column , rating_column):
    '''
   Argument:
       data frame of file
   return:
       data frame with two columns one of text review second is 1 positive or 0 negative
    '''
    positive_reviews = df[df[rating_column] > 3]
    print("We have " + str(len(positive_reviews)) + " positive Reviews")
    negative_reviews = df[df[rating_column] <= 3]
    print("We have " + str(len(negative_reviews)) + " negative Reviews")

# Now get the text reviews for each index and its rate
    positive_reviews = positive_reviews.loc[:, [review_column, rating_column]]
    negative_reviews = negative_reviews.loc[:, [review_column, rating_column]]
    positive_reviews[rating_column] = 1
    negative_reviews[rating_column] = 0
# you will see in the print how looks like the rate of each review as we change

    print("Now We have just the needed columns from the data frame", positive_reviews[:5])
    print("#"*80)
    print("Now We have just the needed columns from the data frame", negative_reviews[:5])
    return positive_reviews, negative_reviews


# In[3]:


def combine_positive_negative_reviews(positive_reviews, negative_reviews):
    '''
    Arguments:
        2 data frames each with 2 columns
    return:
        one data frame contain the two column
    
    '''
    combined_dfs = pd.concat([positive_reviews,negative_reviews], ignore_index=True)
    print("The compined data frame ", combined_dfs[:5])
    print("The compined data frame ", combined_dfs[-5:-1]) # two show negatives also
# next we have a function that shuffle these reviews because of future work
    return combined_dfs


# In[4]:


try:
    df = pd.read_csv('../csv_files/1429_1.csv')
    os.remove('../csv_files/1429_1.csv')
except Exception as e:
    file = open("../logs_files/file_read_error.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines


# In[5]:


# the line below return a data frame with 2 columns for each varaibles 
# text reviews and positive or negative as 1,0


# In[6]:


try:
    positive_reviews, negative_reviews = reviews_handling(df, 'reviews.text', 'reviews.rating')
    first_combined = combine_positive_negative_reviews(positive_reviews, negative_reviews)
except Exception as e:
    file = open("../logs_files/reviews_handling.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines


# In[7]:


# read another file
try:
    df = pd.read_csv('../csv_files/Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv') 
    os.remove('../csv_files/Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv')
    len(df)
except Exception as e:
    file = open("../logs_files/file_read_error.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines


# In[8]:


try:
    positive_reviews, negative_reviews = reviews_handling(df, 'reviews.text', 'reviews.rating')
    second_combine = combine_positive_negative_reviews(positive_reviews, negative_reviews)
    aggregation_combined = combine_positive_negative_reviews(first_combined, second_combine)
except Exception as e:
    file = open("../logs_files/reviews_handling.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines


# In[9]:


# read another file
try:
    df = pd.read_csv('../csv_files/Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv') 
    os.remove('../csv_files/Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv')
    len(df)
except Exception as e:
    file = open("../logs_files/file_read_error.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines


# In[10]:


try:
    positive_reviews, negative_reviews = reviews_handling(df, 'reviews.text', 'reviews.rating')
    third_combine = combine_positive_negative_reviews(positive_reviews, negative_reviews)
    aggregation_combined = combine_positive_negative_reviews(aggregation_combined, third_combine)
except Exception as e:
    file = open("../logs_files/reviews_handling.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines


# In[11]:


# shuffle all reviews
def shuffle_dataframe_of_reviews(df):
    '''
        A function return one data fram but with shuffled rows
    '''
    df = df.sample(frac=1).reset_index(drop=True)
    return df


# In[12]:


try:
    aggregation_combined_shuffled = shuffle_dataframe_of_reviews(aggregation_combined)
    print(aggregation_combined[:20]) # now you can see before shuffle
    print(aggregation_combined_shuffled[:20]) # and you can see after shuffle
    currentDT = str(datetime.datetime.now())
    currentDT
    aggregation_combined_shuffled.to_csv('../csv_files/last_time_combined_reviews_' + currentDT +'.csv', index=False)
    df = pd.read_csv('../csv_files/last_time_combined_reviews_' + currentDT +'.csv')
    print(df.head())
except Exception as e:
    file = open("../logs_files/shuffle_dataframe_of_reviews.log","+a")
    file.write("\n" 
               + str(e) + "\n" + "#" *99 + "\n") # "#" *99 as separated lines



# ### function below to handle reviews
# because of sometimes I classified handlabel reviews, so the file has more than 20 thounsand of reviews, so each time i classified some of these reviews need to append to other classified file for using later then remove these classified reviews from the file.

# In[13]:


def handle_classifed_reviews(file_reviews, 
                             file_classified_reviews, number_of_classifed_reviews):
    '''
    Arguments:
        file reviews: this file has some of reviews classified but not all so,
        number_of_classifed_reviews: we send to cut from and append to,
        file_classified_reviews: which has all of classifed reviews
    return classified file, file_reviews after cuting the number_of_classifed_reviews from it
    '''
# get classifed reviews
    df_classifed_reviews = file_reviews[:number_of_classifed_reviews]
    df_classifed_reviews.dropna(inplace=True) # may some of rows are empty
    df_classifed_reviews = df_classifed_reviews.reset_index(drop=True)
# resave file after cut classifed reviews
    file_reviews = file_reviews.drop(file_reviews.index[:number_of_classifed_reviews])
    file_reviews = file_reviews.reset_index(drop=True)
    file_reviews.to_csv('../csv_files/all_file_reviews.csv',index = False, header=True)
    
# append classified reviews to classifed file
    file_classified_reviews = file_classified_reviews.append(df_classifed_reviews)
    file_classified_reviews = file_classified_reviews.reset_index(drop=True)
    file_classified_reviews.to_csv('../csv_files/file_classified_reviews.csv', index = False, header=True)
    return file_reviews, file_classified_reviews
    


# In[ ]:




