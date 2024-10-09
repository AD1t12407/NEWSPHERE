import os
import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from voice import audio, get_supported_languages  # Import necessary functions from voice.py
from google.cloud import texttospeech 

# Set the page layout to wide mode
st.set_page_config(page_title="NewsSphere", layout="wide")

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def fetch_news(api_key, category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}&country=us"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        st.error("Failed to fetch news")
        return []

def analyze_sentiment(content):
    score = analyzer.polarity_scores(content)
    sentiment = "Neutral"
    if score['compound'] > 0.05:
        sentiment = "Positive"
    elif score['compound'] < -0.05:
        sentiment = "Negative"
    return sentiment

def display_news(articles):
    for idx, article in enumerate(articles):
        col1, col2 = st.columns([1.5, 3])  # Adjust the column width ratio for larger images

        # Display article image
        with col1:
            if article.get('urlToImage'):
                st.image(article['urlToImage'], width=250)  # Increased image size
            st.markdown(f"[Read Full Article]({article['url']})")

        # Display article content and sentiment
        with col2:
            st.subheader(article['title'])
            description = article.get('description') or "No description available"
            st.write(description)
            st.write(f"**Source**: {article['source']['name']}")
            sentiment = analyze_sentiment(description)
            st.write(f"**Sentiment**: {sentiment}")

            # Create a unique key for each button using the article index and article title
            convert_button_key = f"convert_button_{idx}_{article['title'][:10].replace(' ', '_')}"
            # Create a unique key for the selectbox
            language_select_key = f"language_select_{idx}_{article['title'][:10].replace(' ', '_')}"
            languages = get_supported_languages()  # Fetch supported languages
            selected_language = st.selectbox("Select Language", languages, 
                                              index=languages.index("en-US") if "en-US" in languages else 0,
                                              key=language_select_key)  # Use unique key for selectbox

            if st.button("Convert to Audio", key=convert_button_key):
                # Convert article description to audio using voice.py
                gender = texttospeech.SsmlVoiceGender.NEUTRAL  # Specify the voice gender
                audio_data = audio(description, selected_language, gender)
                st.audio(audio_data, format='audio/mp3')

        st.markdown("---")


def personalized_news(api_key, preferences):
    st.subheader("Personalized News Digest")
    for category in preferences:
        st.write(f"### {category.capitalize()} News")
        articles = fetch_news(api_key, category)
        display_news(articles)

def main():
    st.title("📰 NewsSphere - Your Personalized News Experience")

    # Replace 'your_api_key' with your actual API key or store in Streamlit secrets
    api_key = '9c364d44f202437fa167782d1d075057'

    # Sidebar with category filter
    st.sidebar.header("Select Category")
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    selected_category = st.sidebar.selectbox("Select Category", categories)

    # Option to show personalized news
    personalized = st.sidebar.checkbox("Show Personalized News")
    if personalized:
        preferences = st.sidebar.multiselect("Select your preferred categories", categories)
        if preferences:
            personalized_news(api_key, preferences)
        else:
            st.sidebar.write("Select at least one category to get personalized news")

    # Display real-time news
    if selected_category:
        st.subheader(f"📰 {selected_category.capitalize()} News")

        # Fetch and display the news articles
        articles = fetch_news(api_key, selected_category)
        display_news(articles)

        # Show the last updated time
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()