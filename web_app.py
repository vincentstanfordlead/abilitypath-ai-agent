"""
Simple Web Application for the AI Screening Agent
This creates a basic web interface so you can chat with the agent in a browser
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from screening_agent import ScreeningAgent
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management
CORS(app)

# Store agents per session (in production, use Redis or database)
agents = {}


def get_agent(session_id):
    """Get or create an agent for this session"""
    if session_id not in agents:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        agents[session_id] = ScreeningAgent(api_key)
    return agents[session_id]


@app.route('/')
def home():
    """Serve the main chat interface"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    
    try:
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(16)
        
        session_id = session['session_id']
        
        # Get user message
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get agent and process message
        agent = get_agent(session_id)
        result = agent.chat(user_message)
        
        return jsonify({
            'response': result['response'],
            'recommendations_provided': result.get('recommendations_provided', False),
            'collected_info': result.get('collected_info', {})
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the conversation"""
    
    try:
        if 'session_id' in session:
            session_id = session['session_id']
            if session_id in agents:
                agents[session_id].reset_conversation()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Check if the API is working and OpenAI key is configured"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    return jsonify({
        'status': 'ok',
        'openai_configured': bool(api_key and api_key != 'your_openai_api_key_here')
    })


if __name__ == '__main__':
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n" + "="*60)
        print("⚠️  WARNING: OpenAI API key not configured!")
        print("="*60)
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Get your key from: https://platform.openai.com/api-keys")
        print("\n" + "="*60 + "\n")
    
    print("\n" + "="*60)
    print("🚀 Starting AbilityPath Screening Agent")
    print("="*60)
    print("\nAccess the web interface at: http://localhost:5002")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
