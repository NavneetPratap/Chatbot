from flask import Flask, render_template, request
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from googlesearch import search
from deep_translator import GoogleTranslator
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()
translator = GoogleTranslator(source = 'auto', target = 'en')

def preprocess(user_input):
    tokens = word_tokenize(user_input)
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return lemmatized_tokens

import random

responses = {
    "greet": ["Hello!", "Hi there!", "Greetings!"], 
    "ask_name": ["I'm your friendly chatbot!", "You can call me Bot.", "I am a chatbot created to assist you."], 
    "farewell": ["Goodbye!", "See you later!", "Take care!"]
}

def search_web(query):
    results = search(query, num_results = 5)
    return list(results)

def get_response(user_input):
    tokens = preprocess(user_input)
    try:
        if "hi" in tokens or "hello" in tokens:
            return random.choice(responses["greet"])
        elif "name" in tokens:
            return random.choice(responses["ask_name"])
        elif "bye" in tokens:
            return random.choice(responses["farewell"])
        elif "search" in tokens:
            query = " ".join(tokens[tokens.index("search") + 1:])
            results = search_web(query)
            if results:
                return f"results for '{query}':\n" + "\n".join(results)
            else:
                return "Cannot find anything!"
        elif "translate" in tokens:
            text_to_translate = " ".join(tokens[1:])
            translation = translator.translate(text_to_translate, dest = 'en')
            translated_text = translator.translate(text_to_translate)
            return f"Original : {text_to_translate}\nTranslation(en): {translated_text}"    
        else:
            return "Write it in different way!"
    except Exception as e:
        return f"An error occured: {e}"
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_input = request.args.get("msg")
    return get_response(user_input)

if __name__ == "__main__" :
    app.run(debug = True)       
