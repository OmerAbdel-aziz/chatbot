import os
import logging
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging with clear format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Get environment variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_secret_token")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    WhatsApp Cloud API webhook endpoint
    """
    
    if request.method == 'GET':
        # Handle verification challenge from Meta
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        logger.info(f"Webhook verification - Mode: {mode}, Token provided: {'Yes' if token else 'No'}")
        
        # Verify the mode and token
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("✅ Webhook verification successful!")
            return challenge, 200
        else:
            logger.warning("❌ Webhook verification failed - Invalid token or mode")
            return 'Forbidden', 403
    
    elif request.method == 'POST':
        # Handle incoming messages from WhatsApp
        try:
            # Get the JSON payload
            data = request.get_json()
            
            # Log the incoming JSON payload
            logger.info(f"Incoming webhook payload: {data}")
            
            # Extract and log message details if available
            if data and 'entry' in data:
                for entry in data['entry']:
                    if 'changes' in entry:
                        for change in entry['changes']:
                            if change.get('field') == 'messages' and 'value' in change:
                                value = change['value']
                                
                                # Check for new messages
                                if 'messages' in value:
                                    for message in value['messages']:
                                        sender = message.get('from', 'Unknown')
                                        message_text = extract_message_text(message)
                                        
                                        # Print clear log line for new message
                                        logger.info(f"📱 NEW MESSAGE - Sender: {sender}, Text: {message_text}")
            
            return 'EVENT_RECEIVED', 200
            
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return 'EVENT_RECEIVED', 200  # Always return 200 to avoid retries

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint to confirm service is running
    """
    return '''
    <h1>WhatsApp Cloud API Webhook Service</h1>
    <p>✅ Service is running successfully!</p>
    <p><strong>Webhook endpoint:</strong> <code>/webhook</code></p>
    <p>This service is ready to receive WhatsApp webhook calls from Meta.</p>
    ''', 200

def extract_message_text(message):
    """
    Extract text content from message based on type
    """
    message_type = message.get('type', '')
    
    if message_type == 'text':
        return message.get('text', {}).get('body', 'No text')
    elif message_type == 'image':
        caption = message.get('image', {}).get('caption', '')
        return f"[Image] {caption}" if caption else "[Image]"
    elif message_type == 'video':
        caption = message.get('video', {}).get('caption', '')
        return f"[Video] {caption}" if caption else "[Video]"
    elif message_type == 'audio':
        return "[Audio message]"
    elif message_type == 'document':
        filename = message.get('document', {}).get('filename', 'Unknown')
        return f"[Document: {filename}]"
    else:
        return f"[{message_type.capitalize()} message]"

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"🚀 Starting WhatsApp webhook service on port {port}")
    logger.info(f"📡 Webhook URL: http://0.0.0.0:{port}/webhook")
    logger.info(f"🔑 Verify token configured: {'Yes' if VERIFY_TOKEN != 'my_secret_token' else 'Using placeholder'}")
    
    # Run the Flask app on 0.0.0.0:5000
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )