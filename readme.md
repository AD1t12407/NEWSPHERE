# NewsSphere

**NewsSphere** is a personalized news aggregator built with Streamlit that fetches the latest articles from various categories using the News API. The app allows users to read articles, analyze sentiment, and convert article descriptions to audio using Google Cloud Text-to-Speech.

## Features

- **Personalized News Digest**: Users can select their preferred categories to receive tailored news articles.
- **Sentiment Analysis**: Analyze the sentiment of each article's description using the VADER sentiment analysis tool.
- **Audio Conversion**: Convert article descriptions into audio with options for different languages and voice genders.
- **User-Friendly Interface**: Easy navigation with a sidebar for category selection.
<img width="1440" alt="Screenshot 2024-10-09 at 4 13 41 PM (2)" src="https://github.com/user-attachments/assets/aa844bc5-4e43-4581-8ed0-76f416f100b8">
![Screenshot 2024-10-09 at 4 13 41 PM](https://github.com/user-attachments/assets/6d315543-c88a-4afc-93e4-b985cb85c84c)


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
