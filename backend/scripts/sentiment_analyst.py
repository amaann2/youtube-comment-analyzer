import pandas as pd
import json
import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import fire

# Download required NLTK data
nltk.download(['vader_lexicon', 'punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words'])

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment_scores = sia.polarity_scores(text)
    print(sentiment_scores)
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def analyze_comments(id):
    # Read comments from data.json
    json_path = f'media/{id}/data.json'
    if not os.path.exists(json_path):
        print(f"No data file found at {json_path}")
        return
        
    with open(json_path) as f:
        data = json.load(f)
    
    # Convert comments to dataframe
    comments = data['comments']
    df = pd.DataFrame(comments)

    # Apply sentiment analysis to comments
    df['sentiment'] = df['comment'].apply(analyze_sentiment)

    # Calculate sentiment distribution
    sentiment_counts = df['sentiment'].value_counts()

    print(sentiment_counts)

    

if __name__ == '__main__':
    fire.Fire(analyze_comments)


    # Process all comments
    # for index, row in df.iterrows():
    #     comment = row['comment']
    #     print('-' * 80)
    #     print(f"\nAnalyzing comment {index + 1}:")
    #     print(f"Comment text: {comment}")
        
    #     tokens = nltk.word_tokenize(comment)
    #     print('Tokens:')
    #     print(tokens)

    #     tagged_tokens = nltk.pos_tag(tokens)
    #     print('Tagged Tokens:')
    #     print(tagged_tokens)

    #     named_entities = nltk.chunk.ne_chunk(tagged_tokens)
    #     print('Named Entities:')
    #     print(named_entities)


        
    #     print('-' * 80)