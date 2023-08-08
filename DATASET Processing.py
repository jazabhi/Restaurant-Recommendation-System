#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from glob import glob as gb
import seaborn as sns
from tabulate import tabulate

dirs = os.listdir("C:\\Users\\KIIT\\Documents\\Python Projects\\Resturant Recomendation System\\zomato_data")
dirs


# In[3]:


len(dirs)


# In[4]:


#storing all the files from every directory
li=[]
for dir1 in dirs:
    files=os.listdir(r"C:/Users/KIIT/Documents/Python Projects/Resturant Recomendation System/zomato_data/"+dir1)
    #reading each file from list of files from previous step and creating pandas data fame    
    for file in files:
        
        df_file=pd.read_csv("C:/Users/KIIT/Documents/Python Projects/Resturant Recomendation System/zomato_data/"+dir1+"/"+file,quotechar='"',delimiter="|")
#appending the dataframe into a list
        li.append(df_file.values)

print(len(li))


# In[5]:


#numpys vstack method to append all the datafames to stack the sequence of input vertically to make a single array
df_np=np.vstack(li)

#no of rows is represents the total no restaurants ,now of coloumns(12) is columns for the dataframe
print(df_np.shape)

#creating final dataframe from the numpy array
df_final=pd.DataFrame(df_np)


# In[6]:


# adding the header columns
df_final = pd.DataFrame(df_final.values, columns=["NAME",
                                                   "PRICE",
                                                   "CUISEN_CATEGORY",
                                                   "CITY",
                                                   "REGION",
                                                   "URL",
                                                   "PAGE NO",
                                                   "CUISEN TYPE",
                                                   "TIMING",
                                                   "RATING_TYPE",
                                                   "RATING",
                                                   "VOTES"])

# displaying the dataframe
df_final


# In[32]:


#removing unwanted columns
df_final.drop(columns=["PAGE NO"],axis=1,inplace=True)
df_final.drop(columns=["TIMING"],axis=1,inplace=True)
df_final.drop(columns=["VOTES"],axis=1,inplace=True)
df_final.drop(columns=["CUISEN TYPE"],axis=1,inplace=True)


# In[33]:


df_final


# In[13]:


#lets count how many unique cities are there 

df_final["CITY"].unique()


# In[14]:


len(df_final["CITY"].unique())


# In[15]:


#Deleting all the rows which contain restaurants which are yet to open or temporarilt closed
df_final = df_final.drop(df_final[(df_final['RATING'] == 'Opening') | (df_final['RATING'] == 'Temporarily')].index)
df_final


# In[20]:


#finding all the rows where rating is NEW
new_rating_df = df_final[df_final['RATING'] == "NEW"]
new_rating_df

#Replacing all the NEW to 0.1
df_final['RATING'] = df_final['RATING'].replace('NEW', 0.1)

df_final


# In[25]:


#Displaying all the unrated restaurants ratings (-)
new_rating_df = df_final[df_final['RATING'] == "-"]
new_rating_df

#Replacing all the unrated restaurants ratings from - to 0
df_final['RATING'] = df_final['RATING'].replace('-', 0)
df_final


# In[26]:


#making all the strings in the city column uppercase
df_final["CITY"] = df_final["CITY"].str.upper()
df_final


# In[35]:


#Adding serial number
df_final.insert(0, 'Sr No', range(1, len(df_final)+1))
df_final


# In[36]:


#making all the strings in the CUISEN_CATEGORY column uppercase
df_final["CUISEN_CATEGORY"] = df_final["CUISEN_CATEGORY"].str.upper()
df_final


# In[37]:


#Changing some Column names
df_final.rename(columns={"CUISEN_CATEGORY": "CUISINE_CATEGORY"}, inplace=True)
df_final.rename(columns={"RATING_TYPE": "OVERALL"}, inplace=True)
df_final


# In[38]:


df_final.to_csv('restaurants.csv', index=False)

