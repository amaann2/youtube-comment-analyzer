import re
from typing import Counter
from app.helpers.extract_data import get_video_id_from_url, get_video_details, get_comments
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
async def process_youtube_data(url: str, max_comments: int = 6000):
    """
    Orchestrates the extraction and saving of YouTube video details and comments.
    Args:
        url: The YouTube video URL.
    Returns:
        A dictionary containing the processed data.
    """
    video_id = get_video_id_from_url(url)
    video_details = get_video_details(video_id)
    video_details['url'] = url  
    comments = get_comments(video_id, max_comments)
    
   
    data = {
        "video_details": video_details,
        "comments": comments,
    }
    return data

async def sentiment_analysis(data: dict):
    """
    Perform sentiment analysis on the comments of a YouTube video.
    """
    sia = SentimentIntensityAnalyzer()

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
    
    # Add missing sentiment categories with 0 count
    sentiment_categories = ['Positive', 'Negative', 'Neutral']
    for category in sentiment_categories:
        if category not in sentiment_distribution:
            sentiment_distribution[category] = 0
            
    return {
        'sentiment_distribution': sentiment_distribution,
    }
async def analyze_common_words(data: dict):
    """
    Analyze common words from comments and their replies.
    Purpose: Identify recurring topics, suggestions, or keywords.
    """
    comments = data['comments']
    df = pd.DataFrame(comments)
    
    # Combine all comments and replies into one string
    all_text = []
    
    # Add main comments
    all_text.extend(df['comment'].astype(str))
    
    # Add replies
    for comment in comments:
        if 'replies' in comment and comment['replies']:
            for reply in comment['replies']:
                all_text.append(reply['comment'])
    
    # Join all text
    combined_text = ' '.join(all_text)
    
    # Process words
    # Convert to lowercase
    processed_text = combined_text.lower()
    
    # Tokenize into words
    words = processed_text.split()
    
    # Remove stopwords, punctuation and numbers
    stop_words = set(stopwords.words('english'))
    words = [word for word in words 
             if word not in stop_words
             and word.isalnum()
             and not word.isnumeric()]
    
    # Count frequencies
    word_freq = Counter(words)
    
    # Get top 20 words
    return {
        'common_words': dict(word_freq.most_common(20))
    }

async def get_top_ten_comments(data: dict):
    """
    Get the top ten comments sorted by engagement (likes and replies).
    Purpose: Show which comments received the most likes or replies to identify popular discussions.
    """
    comments = data['comments']
    
    # Calculate engagement score for each comment (likes + number of replies)
    for comment in comments:
        engagement_score = comment.get('like_count', 0)
        if 'replies' in comment:
            engagement_score += len(comment['replies'])
            # Also add likes from replies
            for reply in comment['replies']:
                engagement_score += reply.get('like_count', 0)
        comment['engagement_score'] = engagement_score
    
    # Sort comments by engagement score
    sorted_comments = sorted(comments, key=lambda x: x['engagement_score'], reverse=True)
    
    # Get top 10 comments
    top_ten = sorted_comments[:10]
    
    return {
        'top_comments': top_ten
    }
