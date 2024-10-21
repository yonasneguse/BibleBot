
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

app = Flask(__name__)

def get_bible_verse(keyword):
    try:
        r = requests.get(f'https://bible-api.com/{keyword}')
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            quote = f'{data["reference"]}: {data["text"]} ({data["translation_name"]})'
            return quote
        else:
            return "I couldn't find a verse with that keyword, please try again."
    except Exception as e:
        return f"Error retrieving verse: {str(e)}"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    tokens = word_tokenize(incoming_msg)

    if 'verse' in tokens:
        if len(tokens) > 2:  # if user provides multiple keywords
            keyword = tokens[-1]
            quote = get_bible_verse(keyword)
        else:
            # if no specific keyword provide a random verse
            r = requests.get('https://bible-api.com/?random=verse')
            if r.status_code == 200:
                data = r.json()
                quote = f'{data["reference"]} ({data["text"]}) ({data["translation_name"]})'
            else:
                quote = 'I could not retrieve a random Bible verse at this time, sorry.'
        msg.body(quote)
        responded = True
    
    if not responded:
        msg.body('I only know about Bible verses! Try asking for a verse with a specific keyword.')
    
    return str(resp)

