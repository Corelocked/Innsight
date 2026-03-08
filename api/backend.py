import os
import pandas as pd
from collections import Counter
from functools import lru_cache
from fuzzywuzzy import fuzz, process
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# --- Cached NLTK resources for better cold start performance ---
_stop_words_cache = None

def get_stopwords():
    """Lazy-load and cache stopwords to improve cold start times."""
    global _stop_words_cache
    if _stop_words_cache is not None:
        return _stop_words_cache
    
    try:
        _stop_words_cache = set(stopwords.words('english'))
    except Exception:
        try:
            # Download NLTK data if not available (only happens once)
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            _stop_words_cache = set(stopwords.words('english'))
        except Exception:
            # Fallback to common stopwords if download fails
            _stop_words_cache = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'}
    return _stop_words_cache


# --- Text preprocessing with caching ---
@lru_cache(maxsize=256)
def preprocess_text(text):
    """Preprocess text with caching for repeated queries."""
    try:
        tokens = word_tokenize(text.lower())
    except Exception:
        # Fallback to simple split if NLTK tokenizer fails
        tokens = text.lower().split()
    return tuple(word for word in tokens if word.isalpha())  # Return tuple for caching


def get_frequent_words(df, threshold=5):
    """Identify frequently occurring words to filter out."""
    word_count = Counter()
    for question in df['Question']:
        words = preprocess_text(question)
        word_count.update(words)
    return {word for word, count in word_count.items() if count >= threshold}


def load_inquiries(file_path):
    """Load and preprocess inquiry data with error handling."""
    try:
        df = pd.read_csv(file_path)
        df['Question'] = df['Question'].astype(str).str.strip()

        stop_words = get_stopwords()
        frequent_words = get_frequent_words(df)
        
        def process_question(question):
            words = preprocess_text(question)
            return ' '.join([w for w in words if w not in frequent_words and w not in stop_words])
        
        df['Processed Question'] = df['Question'].apply(process_question)
        inquiries_dict = dict(zip(df['Processed Question'].str.lower(), df['Response']))
        return inquiries_dict, frequent_words
    except FileNotFoundError:
        print(f"Error: Inquiry file not found at {file_path}")
        return {}, set()
    except Exception as e:
        print(f"Error loading inquiries: {e}")
        return {}, set()


# Resolve the path to the CSV in the same folder (api/)
# First check local api/ folder, then fallback to repo structure for dev
DEFAULT_INQUIRIES_PATH = os.path.join(os.path.dirname(__file__), 'inquiries.csv')
if os.path.exists(DEFAULT_INQUIRIES_PATH):
    inquiries_path = DEFAULT_INQUIRIES_PATH
else:
    # Fallback for local dev when running from repo root
    fallback_path = os.path.join(os.path.dirname(__file__), '..', 'voice-order-system', 'inquiries.csv')
    inquiries_path = fallback_path if os.path.exists(fallback_path) else 'inquiries.csv'

inquiry_responses, frequent_words = load_inquiries(inquiries_path)


@lru_cache(maxsize=128)
def match_inquiry(user_input):
    """Perform fuzzy matching with caching for repeated queries."""
    if not frequent_words or not inquiry_responses:
        return None
    
    # Preprocess and filter
    tokens = preprocess_text(user_input)
    user_input_processed = ' '.join([w for w in tokens if w not in frequent_words])
    
    if not user_input_processed.strip():
        return None
    
    try:
        best_match, score = process.extractOne(
            user_input_processed.lower(), 
            inquiry_responses.keys(), 
            scorer=fuzz.token_set_ratio
        )
        if score and score >= 75:
            return inquiry_responses.get(best_match)
    except Exception as e:
        print(f"Error in fuzzy matching: {e}")
    
    return None


# --- Intent classification with optimized keyword matching ---
INTENT_KEYWORDS = {
    "Room Service Order": ["order", "food", "room service", "meal", "menu", "snack", "drink", "coffee", "tea", "breakfast", "lunch", "dinner"],
    "Amenities Request": ["towel", "pillows", "extra blanket", "bathroom", "toiletries", "shampoo", "soap", "hair dryer", "robe"],
    "Food Inquiry": ["ice cream", "food", "meal", "snack", "dessert", "order food"],
    "Feedback or Complaint": ["complaint", "feedback", "issue", "problem"],
    "Greeting": ["hi", "hello", "hey", "good morning", "good evening"],
}

INTENT_RESPONSES = {
    "Room Service Order": "Thank you for your order! Your food will be delivered shortly.",
    "Amenities Request": "Your request for additional amenities has been noted and will be sent to your room soon.",
    "Food Inquiry": "Ice cream sounds great! Let me place that order for you right away.",
    "Feedback or Complaint": "We're sorry to hear that. Could you please provide more details about the issue?",
    "Greeting": "Hello! How can I assist you today?",
}


@lru_cache(maxsize=256)
def determine_intent(user_input):
    """Determine user intent with caching for common queries."""
    # First check inquiry database
    inquiry_response = match_inquiry(user_input)
    if inquiry_response:
        return ("Inquiry", inquiry_response)

    user_lower = user_input.lower()
    
    # Check for greeting first (most specific)
    if any(k in user_lower for k in INTENT_KEYWORDS.get("Greeting", [])):
        return ("Greeting", INTENT_RESPONSES["Greeting"])

    # Check other intents
    for intent, keywords in INTENT_KEYWORDS.items():
        if intent != "Greeting" and any(keyword in user_lower for keyword in keywords):
            return (intent, INTENT_RESPONSES.get(intent, "I'm sorry, I didn't quite understand your request."))

    return ("Unknown", "I'm sorry, I didn't quite understand your request.")


def handle_user_input(user_input):
    """Main handler for user input with validation."""
    if not user_input or not user_input.strip():
        return "Please provide a valid request."
    
    try:
        intent, response = determine_intent(user_input.strip())
        return response
    except Exception as e:
        print(f"Error handling user input: {e}")
        return "An error occurred processing your request. Please try again."
