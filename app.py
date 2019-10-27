import numpy as np
from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt


app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

def percentage(part, whole):
  return 100 * float(part)/float(whole)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])




def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
    
    consumerKey="58QZ1yew4RiK6Kdh1cFOrlqPO"
    consumerSecret="pvS4xUHSP84CNsWlxP6YH8rxgFP7ZJzUmVCekHvDuI0vk5bkGb"
    accessToken="598985744-sG96Q21U46ehBRqeLs0kfJhz6MEcX47opk089rbX"
    accessTokenSecret="y8nziEiYJLpWiFcbVEgccYClOrcQWbn3gHSQZorwKdXBn"

    auth =tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api= tweepy.API(auth)

    #searchTerm=input("enter keyword/hashtag to search about: ")
    #noOfSearchTerms=int(input("Enter how many tweets to analyze: "))

    tweets=tweepy.Cursor(api.search, q=final_features[0][0], language="English").items(int(final_features[0][1]))
    noOfSearchTerms=int(final_features[0][1])
    positive=0
    negative=0
    neutral=0
    polarity=0
    for tweet in tweets:
      analysis=TextBlob(tweet.text)
      polarity+=analysis.sentiment.polarity
      
      if(analysis.sentiment.polarity == 0):
        neutral+=1
      elif(analysis.sentiment.polarity < 0):
        negative+=1
      elif(analysis.sentiment.polarity > 0):
        positive+=1
    positive=percentage(positive, noOfSearchTerms)
    negative=percentage(negative, noOfSearchTerms)
    neutral=percentage(neutral, noOfSearchTerms)
    polarity=percentage(polarity,noOfSearchTerms)

    positive=format(positive,'0.2f')
    negative=format(negative,'0.2f')
    neutral=format(neutral,'0.2f')

    #print("How people are reacting on "+searchTerm+" by analyzing "+str(noOfSearchTerms)+" Tweets.")

    if(polarity == 0.00):
      output="Neutral"
    elif(polarity < 0.00):
      output="Negative"
    elif(polarity > 0.00):
      output="Positive"
    labels=['Positive ['+str(positive)+'%]', 'Neutral ['+str(neutral)+'%]', 'Negative ['+str(negative)+'%]']
    sizes=[positive,neutral,negative]
    colors=['yellowgreen','gold','red']
    patches, texts=plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("How people are reacting on "+final_features[0][0]+" by analyzing "+str(noOfSearchTerms)+" Tweets.")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    return render_template('index.html', prediction_text='Overall Sentiment : {}'.format(output))



if __name__ == "__main__":
    app.run(debug=True)