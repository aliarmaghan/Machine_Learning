#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests


# In[2]:


df = pd.DataFrame()


# In[3]:


for i in range(1,471):
    resp1 = requests.get('https://api.themoviedb.org/3/movie/top_rated?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US&page={}'.format(i))
    tmp_df1 = pd.DataFrame(resp1.json()['results'])[['title','overview','genre_ids']]
    df = df.append(tmp_df1,ignore_index=True)


# In[4]:


## this is used for rename columns name
# df.rename(columns = {'genre_ids':'id'}, inplace = True)abs


# In[11]:


df_exploded = df.explode('genre_ids')


# In[35]:


df_exploded
# df


# In[41]:


resp2 = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
df2 = pd.DataFrame(resp2.json()['genres'])


# In[43]:


df2


# In[44]:


# Merge the DataFrames based on the 'genre_id' column
merged_df = pd.merge(df_exploded,df2,left_on='genre_ids', right_on='id',how='left')

# Select the desired columns
final_df = merged_df[['title', 'overview', 'name']]
final_df

final_df['name'] = final_df['name'].fillna('')

# Convert all values in 'name' column to string
final_df['name'] = final_df['name'].astype(str)


# In[45]:


df_final = final_df.groupby(['title','overview'])['name'].apply(lambda x: ', '.join(x)).reset_index()
df_final


# # Text Preprocessing on overview:

#  **Lowercasing**

# In[46]:


df_final['overview'] = df['overview'].str.lower()
df_final


# **Removing HTML-tags**

# In[47]:


import re
def remove_html_tags(text):
    pattern = re.compile('<.*>')
    return pattern.sub(r'', text)


# In[48]:


df_final['overview'] = df_final['overview'].apply(remove_html_tags)
df_final


# **Remove URLs**

# In[49]:


def remove_url(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    return pattern.sub(r'', text)


# In[50]:


df_final['overview'] = df_final['overview'].apply(remove_url)
df_final


# **Remove Punctuation**

# In[51]:


import string,time
exclude = string.punctuation


# In[52]:


def remove_punc1(text):
    return text.translate(str.maketrans('','',exclude))


# In[53]:


df_final['overview'] = df_final['overview'].apply(remove_punc1)
df_final


# **Spell Correction**

# In[55]:


# from textblob import TextBlob


# **Stopper removal**

# In[66]:


import nltk
nltk.download('stopwords')


# In[67]:


from nltk.corpus import stopwords


# In[68]:


def remove_stopwords(text):
    new_text = []
    
    for word in text.split():
        if word in stopwords.words('english'):
            new_text.append('')
        else:
            new_text.append(word)
    x = new_text[:]
    new_text.clear()
    return " ".join(x)


# In[69]:


df_final['overview'] = df_final['overview'].apply(remove_stopwords)
df_final


# **Tokenization**

# In[70]:


from nltk.tokenize import word_tokenize, sent_tokenize


# In[71]:


word_tokenize(df_final['overview'] )


# In[ ]:




