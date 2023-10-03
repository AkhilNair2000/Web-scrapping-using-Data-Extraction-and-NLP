#!/usr/bin/env python
# coding: utf-8

# ## Importing libraries 
# For each of the articles, given in the input.xlsx file, extract the article text and save the extracted article in a text file with URL_ID as its file name.

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


# In[2]:


input_df = pd.read_excel(r'C:\Users\Akhil\Desktop\Input.xlsx')


# In[3]:


input_df.head() 
input_df.info() 


# In[4]:


# urls = input_df[['URL_ID', 'URL']].to_dict('records')


# In[5]:


url_ids = input_df['URL_ID']
urls = input_df['URL']


# In[6]:


output_df = pd.DataFrame(columns=["URL_ID",
                                  "URL",
                                  "positive_score",
                                  "negative_score",
                                  "polarity_score",
                                  "subjectivity_score",
                                  "avg_sentence_length",
                                  "percentage_of_complexwords",
                                  "fog_index",
                                  "avg_number_of_words_per_sentence",
                                  "complex_word_count",
                                  "word_count",
                                  "syllables_per_word",
                                  "personal_pronouns",
                                  "avg_word_length"])


# In[7]:


for url in urls:
    text =""
    count = 0
    sentiment_score = 0
    positive_score = 0
    negative_score = 0
    neutral_score = 0
    total_syllables = 0
    complex_words = 0
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article = soup.find(attrs={'class':'td-post-content'})
    
    if article:    
        text += article.get_text()
        blob = TextBlob(text)
        sentences = blob.sentences
        words = blob.words
        syllables = nltk.corpus.cmudict.dict()
#         with open(f"{url}.txt", "w") as file:
#             file.write(text)
    
        for sentence in sentences:
            
            if sentence.sentiment.polarity > 0:
                positive_score +=  1
            elif sentence.sentiment.polarity < 0:
                negative_score +=  1
            else:
                neutral_score +=  1
            sentiment_score += sentence.sentiment.polarity

        for word in words:
            syllables = 0
            word = word.lower()
            try:

                if word in nltk.corpus.words.words():
                    syllables =len(nltk.corpus.cmudict.dict()[word][0])
                    print(nltk.corpus.cmudict.dict()[word][0])
                    total_syllables += syllables
                    if syllables >= 3:
                        complex_words += 1
            except KeyError:
                    print(f"{word} is not present in the dictionary")
        for char in word:
            if char.isalpha():
                count += 1
        
         
                
                
        personal_pronouns = word_tokenize(text)
        personal_pronouns_count = len([pnoun for pnoun in personal_pronouns if pnoun.lower() in ['i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']])        
                 
        word_count = len(words)
        avg_word_lenght = word_count / count 
        polarity_score = (positive_score - negative_score) / (positive_score + negative_score) + 0.00001
        syllables_per_word = total_syllables / word_count        
        avg_sentence_length = sum(len(s.words) for s in sentences) / len(sentences)
        percentage_complex_words = (complex_words / word_count) * 100
        fog_index = 0.4 * (percentage_complex_words + avg_sentence_length)
        
        avg_words_per_sentence = word_count / len(sentences)
        
        subjectivity_score = sentiment_score / word_count + 0.000001
        

       
    else:     
        print(f"URL doesn't exist: {url}")
        
#     print("Positive score: ", positive_score)
#     print("Negative score: ", negative_score)
#     print("Polarity score: ", polarity_score)
#     print("Subjectivity score: ", subjectivity_score)
    
#     print("Percentage of complex words: ", percentage_complex_words)
#     print("Fog index: ", fog_index)
#     print("Average Number of words per sentence: ", avg_sentence_length)
#     print("Complex words: ", complex_words)
#     print("Word count: ", word_count)
#     print("Syllables per word: ", syllables_per_word)
#     print
#     print("AVG word Length: " , avg_word_lenght)
    output_df = output_df.append({
            "URL_ID": url_ids, 
            "URL": url, 
            "positive_score": positive_score, 
            "negative_score": negative_score, 
            "polarity_score": polarity_score, 
            "subjectivity_score": subjectivity_score, 
            "avg_sentence_length": avg_sentence_length, 
            "percentage_of_complexwords": percentage_complex_words, 
            "fog_index": fog_index, 
            "avg_number_of_words_per_sentence": avg_words_per_sentence, 
#             "complex_word_count": complex_word_count, 
            "word_count": word_count,
            "syllables_per_word" : syllables_per_word,
            "personal_pronouns" : "",
            "avg_word_length" : avg_word_lenght                              
            },ignore_index=True
            )
    
    


# In[8]:


output_df = output_df.append({
            "URL_ID": url_ids, 
            "URL": url, 
            "positive_score": positive_score, 
            "negative_score": negative_score, 
            "polarity_score": polarity_score, 
            "subjectivity_score": subjectivity_score, 
            "avg_sentence_length": avg_sentence_length, 
            "percentage_of_complexwords": percentage_complex_words, 
            "fog_index": fog_index, 
            "avg_number_of_words_per_sentence": avg_words_per_sentence, 
#             "complex_word_count": complex_word_count, 
            "word_count": word_count,
            "syllables_per_word" : syllables_per_word,
            "personal_pronouns" : "",
            "avg_word_length" : avg_word_lenght                              
            },ignore_index=True
            )


# In[9]:


# output_df = output_df.append({
# "URL_ID": url_id, 
# "URL": url, 
# "positive_score": positive_score, 
# "negative_score": negative_score, 
# "polarity_score": polarity_score, 
# "subjectivity_score": subjectivity_score, 
# "avg_sentence_length": avg_sentence_length, 
# "percentage_of_complexwords": percentage_complex_words, 
# "fog_index": fog_index, 
# "avg_number_of_words_per_sentence": avg_words_per_sentence, 
# "complex_word_count": complex_word_count, 
# "word_count": word_count,
# "syllables_per_word" : syllables_per_word,
# "personal_pronouns" : "",
# "avg_word_length" : avg_word_lenght                              
#                              },ignore_index=True
# )


# In[10]:


output_df.to_excel(r'C:\Users\Akhil\Downloads\Output Data Structure.xlsx', index=True, header=True)


# In[ ]:




