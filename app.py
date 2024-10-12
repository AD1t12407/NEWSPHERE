import os
import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from voice import audio, get_supported_languages  # Import necessary functions from voice.py
from google.cloud import texttospeech
import json
from google.oauth2 import service_account

# Set the page layout to wide mode
st.set_page_config(page_title="NewsSphere", layout="wide")

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Load API key and Google credentials from environment variables or Streamlit secrets
api_key = os.getenv('API_KEY') or st.secrets["API_KEY"]

# Load Google credentials (from secrets if deployed)
service_account_info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
credentials = service_account.Credentials.from_service_account_info(service_account_info)

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
        col1, col2 = st.columns([1.5, 3])

        with col1:
            if article.get('urlToImage'):
                st.image(article['urlToImage'], width=250)
            st.markdown(f"[Read Full Article]({article['url']})")

        with col2:
            st.subheader(article['title'])
            description = article.get('description') or "No description available"
            st.write(description)
            st.write(f"**Source**: {article['source']['name']}")
            sentiment = analyze_sentiment(description)
            st.write(f"**Sentiment**: {sentiment}")

            convert_button_key = f"convert_button_{idx}_{article['title'][:10].replace(' ', '_')}"
            language_select_key = f"language_select_{idx}_{article['title'][:10].replace(' ', '_')}"
            languages = get_supported_languages()
            selected_language = st.selectbox("Select Language", languages, 
                                              index=languages.index("en-US") if "en-US" in languages else 0,
                                              key=language_select_key)

            if st.button("Convert to Audio", key=convert_button_key):
                gender = texttospeech.SsmlVoiceGender.NEUTRAL
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

    # Sidebar with category filter
    st.sidebar.header("Select Category")
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    selected_category = st.sidebar.selectbox("Select Category", categories)
    
    # Show subcategories if 'technology' is selected
    if selected_category == 'technology':
        st.sidebar.write("### Select Domain")
        domains = ['blockchain', 'ai', 'data-science', 'quantum-computing', 'robotics', 'bioinformatics']
        selected_domain = st.sidebar.selectbox("Select Domain", domains)
        selected_category = selected_domain  # Update the category to the selected domain

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