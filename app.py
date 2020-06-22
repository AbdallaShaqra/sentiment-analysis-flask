# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:49:29 2020

@author: Abdalla
"""

from flask_cors import CORS ,cross_origin
from flask import Flask ,Response ,request
import json
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import emoji
import re
import datetime



data = pd.read_csv(r"out3.csv",encoding="windows-1256")
print("..................")
max_fatures = 2000
tokenizer = Tokenizer(num_words=max_fatures, split=' ')
tokenizer.fit_on_texts(data['text'].values)
print(tokenizer)

model = load_model('a.h5')

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def listToText(s):  
    
     
    str1 = ""  
    
       
    for i in s:  
        str1 += i+" "   
    
       
    return str1  


def filter_text(e):
    e = re.sub('[a-zA-Z]','' ,e)
    e = re.sub("[÷]",'',e)
    e = re.sub("[×]",'',e)
    e = re.sub("[؛]",'',e)
    e = re.sub("[~]",'',e)
    e = re.sub("[ـ]",'',e)
    e = re.sub("[`]",'',e)
    e = re.sub("[،]",'',e)
    
    return e




def emoji_to_text(text1):
    
    d = emoji.demojize(text1)
    d = d.replace(":"," ")
    d = d.split(" ")
    g = pd.read_csv(r"emoji2.csv",encoding="windows-1256" , sep=";" )
    for i in d:
        try:
            a = g.loc[g['text']==":"+i+":",'translate'].iloc[0]
            #d[d.index(i)] = a
            d.remove(i)
        except IndexError:
            ""
    t = listToText(d)
    c = filter_text(t)
    return c  
def most_frequent(List): 
    if not List:
        return "empty"
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num   
def emoji_to_label(text2):
    list2 = []
    d = emoji.demojize(text2)
    d = d.replace(":"," ")
    d = d.split(" ")
    g = pd.read_csv(r"emoji4.csv",encoding="windows-1256",sep=";")

    for i in d:
        try:
            a = g.loc[g['text']==":"+i+":",'label'].iloc[0]
            #d[d.index(i)] = a
            
            list2.append(a)
        except IndexError:
            ""
    #t = listToText(d)
    #c = filter_text(t)
    #v = space_filter(c)
           
    return most_frequent(list2)    


def output(text):
    
    for i in text:
        #i = emoji_to_text(i)
        te = emoji_to_label(i)

        twt  = [emoji_to_text(i)]
        
        #vectorizing the tweet by the pre-fitted tokenizer instance
        twt = tokenizer.texts_to_sequences(twt)
        #padding the tweet to have exactly the same shape as `embedding_2` input
        twt = pad_sequences( twt, maxlen=238, dtype='int32', value=0)

        sentiment = model.predict(twt,batch_size=1,verbose = 2)[0]

        sym = np.argmax(sentiment)
    
        per =  round(max(sentiment) * 100 ,1 ) 
        
        sntm = ""
        
        
           
        
        if per >= 75:
            if sym == 1:
                sntm ="positive"
                
                
            
            else:
                sntm = "negative"
            report ={
        
        
              
        'sentence':i,
        'symbol': sym,
        'sentiment':sntm,
        'confidence': per
    }    
        
        if per < 75:
            if te == 1 and sym == 1:
                sntm = "positive"
                
                

            
            elif te == 0 and sym == 0:
                
                sntm = "negative"
            
            elif twt[0][-1] == 0 and te is not "empty" :
                
                if te == 0:
                    sntm = "negative"
                else :
                    sntm = "positive"
            
            else: 
                sntm = "neutral"
            
            report ={
        
        
              
        'sentence':i,
        'symbol': sym,
        'sentiment':sntm,
        'confidence': per
    }            
            
                
            


            
            
           
            
            
      
                
            
        
        datetime_object = datetime.datetime.now()
    
        return {'data':{'lang':'ar','created':str(datetime_object),'result':report}}
    
    
    
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
@app.route("/api",methods=['GET'])


def get_tasks():
    
    texts = request.args.getlist("text")
    
  
    b = json.dumps(output(texts),cls = NpEncoder,indent=None,ensure_ascii=False)
    return Response(b,mimetype='application/json')
    #return output(text)
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False,threaded=False)



