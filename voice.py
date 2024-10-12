import os
from google.cloud import texttospeech
from io import BytesIO
import json
from google.oauth2 import service_account
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env for local development
load_dotenv()

# Load Google Cloud credentials from Streamlit secrets or .env file (local)
if "GCP_SERVICE_ACCOUNT" in st.secrets:
    # For Streamlit deployment, load credentials from Streamlit secrets
    service_account_info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
else:
    # For local development, load from GOOGLE_APPLICATION_CREDENTIALS set in .env
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient(credentials=credentials)

def get_supported_languages():
    """Returns a sorted list of supported languages."""
    response = client.list_voices()
    languages = set()
    for voice in response.voices:
        for language_code in voice.language_codes:
            languages.add(language_code)
    return sorted(list(languages))

def synthesize_text(text, language_code, gender):
    """Synthesizes speech from the input string of text."""
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content

def audio(text, language, gender):
    """Returns the audio content of the synthesized speech."""
    audio_content = synthesize_text(text, language, gender)
    return BytesIO(audio_content)

