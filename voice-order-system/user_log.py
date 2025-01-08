import os
import logging
import datetime

# Set up logging configuration
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Set up interaction log file and feedback log file paths
LOG_FILE = os.path.join(LOG_DIR, "interaction_logs.txt")
FEEDBACK_FILE = os.path.join(LOG_DIR, "feedback_logs.txt")

# Configure logging for interaction logs
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG if you want more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Log to console as well for debugging
    ]
)

# Configure feedback logging
feedback_logger = logging.getLogger("feedback")
feedback_logger.setLevel(logging.INFO)
feedback_logger.addHandler(logging.FileHandler(FEEDBACK_FILE))

def log_interaction(transcription, intent, sentiment, response):
    try:
        logging.info(f"Transcription: '{transcription}' | Intent: {intent} | Sentiment: {sentiment} | Response: {response}")
        print("Interaction logged successfully!")  # Debugging message for confirmation
    except Exception as e:
        logging.error(f"Error logging interaction: {str(e)}")  # Optionally log to console or a dedicated error log
        print(f"Error logging interaction: {str(e)}")  # Debugging message

def log_feedback(feedback):
    try:
        feedback_logger.info(f"Feedback: '{feedback}'")
        print("Feedback logged successfully!")  # Debugging message for confirmation
    except Exception as e:
        logging.error(f"Error logging feedback: {str(e)}")  # Optionally log to console or a dedicated error log
        print(f"Error logging feedback: {str(e)}")  # Debugging message

# Test logging to check if the logging system is working
log_interaction("Test transcription", "Test Intent", "Positive", "Test Response")
log_feedback("Test feedback")
