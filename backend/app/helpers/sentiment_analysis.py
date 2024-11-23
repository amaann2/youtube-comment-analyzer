import json
import os
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment_analysis(id: str):
    sia = SentimentIntensityAnalyzer()
    json_path = f'media/{id}/data.json'
    if not os.path.exists(json_path):
        print(f"No data file found at {json_path}")
        return
        
    with open(json_path) as f:
        data = json.load(f)
    
    comments = data['comments']
    df = pd.DataFrame(comments)

    sentiment_details = []
    
    for index, row in df.iterrows():
        comment = row['comment']
        
        sentiment_scores = sia.polarity_scores(comment)
        
        if sentiment_scores['compound'] >= 0.05:
            sentiment = 'Positive'
        elif sentiment_scores['compound'] <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        sentiment_details.append({'sentiment': sentiment})
            
    
    df['sentiment'] = [detail['sentiment'] for detail in sentiment_details]
    sentiment_distribution = df['sentiment'].value_counts().to_dict()
    
    return {
        'sentiment_distribution': sentiment_distribution,
    }

