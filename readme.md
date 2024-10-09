# NewsSphere

**NewsSphere** is a personalized news aggregator built with Streamlit that fetches the latest articles from various categories using the News API. The app allows users to read articles, analyze sentiment, and convert article descriptions to audio using Google Cloud Text-to-Speech.

## Features

- **Personalized News Digest**: Users can select their preferred categories to receive tailored news articles.
- **Sentiment Analysis**: Analyze the sentiment of each article's description using the VADER sentiment analysis tool.
- **Audio Conversion**: Convert article descriptions into audio with options for different languages and voice genders.
- **User-Friendly Interface**: Easy navigation with a sidebar for category selection.

## Technologies Used

- [Streamlit](https://streamlit.io/) - The framework for building the web application.
- [News API](https://newsapi.org/) - To fetch news articles.
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment) - For sentiment scoring.
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech) - For converting text to audio.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Cloud account with Text-to-Speech enabled
- News API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/NewsSphere.git
   cd NewsSphere
   ```
