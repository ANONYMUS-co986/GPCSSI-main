from flask import Flask, request, jsonify, render_template, session, send_from_directory
from flask_cors import CORS
from chatbot_core import CybercrimeChatbot
import os
import traceback

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'supersecretkey'  # Change this in production
CORS(app)

# Store chatbot instance globally (stateless, but we use session for history)
chatbot = CybercrimeChatbot()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat_page():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    # Use session to store conversation history
    if 'history' not in session:
        session['history'] = []
    chatbot.conversation_history = session['history']
    try:
        response = chatbot.get_response(user_message)
        chatbot.conversation_history.append({'role': 'user', 'content': user_message})
        chatbot.conversation_history.append({'role': 'bot', 'content': response})
        session['history'] = chatbot.conversation_history
        return jsonify({'response': response})
    except Exception as e:
        print('API Error:', e)
        traceback.print_exc()
        return jsonify({'response': 'Sorry, an internal error occurred. Please try again later.'}), 500

@app.route('/health')
def health():
    # Simple health check for diagnostics
    status = {'flask': True}
    try:
        # Check if datasets are loaded
        status['cybercrime_data'] = chatbot.df_cybercrime is not None
        status['attacks_data'] = chatbot.df_attacks is not None
        # Check OpenAI API
        status['openai_api'] = chatbot.model is not None
    except Exception as e:
        status['error'] = str(e)
    return jsonify(status)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True) 