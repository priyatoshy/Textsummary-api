
#uvicorn summaryapi:app --reload

#API: APPLICATION PROGRAMMING INTERFACE IS A CONTRACT BETWEEN TWO SYSTEMS FOR
#SHARING RESOURCES/DATA IN A REQUEST RESPONSE SCHEME

#REST API-Representational State Transfer
#IT IS HTTP DEPENDENT API


from cgitb import text
import imp
from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

#----------------------------------------------------------------------

#starting the app
app=FastAPI()



#POST REQUEST WILL REQUIRE A REQUEST BODY
@app.get("/")
def home():
    return {"Data":"Text Summarization"}


#POST ARGUMENT
#Creating A String Class

class Text(BaseModel):
    data:str





#----------------------------------------------------------
#post api for text summarization

@app.post("/create-summary/{summary_heading}")
def summary(summary_heading:str,textdata:Text):


       

        #text summarization functionality

        import spacy
        from  spacy.lang.en.stop_words import STOP_WORDS
        from string import punctuation
        from heapq import nlargest
        from textblob import TextBlob
        nlp=spacy.load('en_core_web_sm')
        text=textdata.data

        #creating stop words
        stopwords=list(STOP_WORDS)

        #loading the text into the nlp module
        doc=nlp(text)

        #computing the result
        #appending punctation
        punctuation+="\n"
        tokens=[token.text for token in doc]
        word_frequencies={}


        #creating a word frequecny table
        #def word_frequency_table_generator()
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in stopwords:
                     if word.text not in word_frequencies.keys():
                        word_frequencies[word.text]=1
                     else:
                        word_frequencies[word.text]+=1




        #normalizing frequency
        max_freqeuncy=max(word_frequencies.values())
        for word in word_frequencies.keys():
                word_frequencies[word]=word_frequencies[word]/max_freqeuncy

        #sentence tokenizations

        sentence_token=[sent for sent in doc.sents]



        #calculating sentence scores based on word score sum

        sentence_scores={}

        for sent in sentence_token:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent]=word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent]+=word_frequencies[word.text.lower()]



        #creating a select length


        select_length=int(len(sentence_scores)*0.3)

        summary=nlargest(select_length,sentence_scores,key=sentence_scores.get)

        #converting to text

        final_summary=[word.text for word in summary]

        #joining into a text
        summary=' '.join(final_summary)

        summaryblob=TextBlob(summary)

        summarySentiment=summaryblob.sentiment
        
        summarySentiment=f"{summarySentiment}"


        

        context={'original':text,'summary':summary,'sentiment':summarySentiment}
        
        context={summary_heading:context}
        
        return context
        #text summarization functionality
    
