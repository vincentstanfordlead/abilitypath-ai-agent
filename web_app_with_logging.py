"""
Web Application with ENHANCED LOGGING
This version has detailed logging so you can see what's happening!

To use: Rename this to web_app.py or run directly:
python3 web_app_with_logging.py
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from screening_agent import ScreeningAgent
import secrets
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Store agents per session
agents = {}

# Create logs directory
os.makedirs('logs', exist_ok=True)

def log_conversation(session_id, user_message, agent_response, collected_info, recommendations_provided):
    """Log conversation to file for later analysis"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id[:8],  # Shortened for privacy
        "user_message": user_message,
        "agent_response": agent_response[:200],  # First 200 chars
        "collected_info": collected_info,
        "recommendations_provided": recommendations_provided
    }
    
    # Save to JSONL file (one JSON object per line)
    with open('logs/conversations.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


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
        
        # 🔍 LOGGING: Print to terminal
        print("\n" + "="*70)
        print(f"📨 NEW MESSAGE from session: {session_id[:8]}...")
        print(f"👤 User: {user_message}")
        print("-"*70)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get agent and process message
        agent = get_agent(session_id)
        result = agent.chat(user_message)
        
        # 🔍 LOGGING: Print agent response
        print(f"🤖 Agent: {result['response'][:150]}...")  # First 150 chars
        print("-"*70)
        print(f"📊 Collected Info:")
        print(f"   Age: {result.get('collected_info', {}).get('age', 'Not yet extracted')}")
        print(f"   Needs: {list(result.get('collected_info', {}).get('needs', {}).keys())}")
        print(f"   Needs count: {len(result.get('collected_info', {}).get('needs', {}))}")
        print("-"*70)
        print(f"{'✅ RECOMMENDATIONS PROVIDED' if result.get('recommendations_provided') else '⏳ Still gathering info'}")
        print("="*70 + "\n")
        
        # 🔍 LOGGING: Save to file
        log_conversation(
            session_id,
            user_message,
            result['response'],
            result.get('collected_info', {}),
            result.get('recommendations_provided', False)
        )
        
        return jsonify({
            'response': result['response'],
            'recommendations_provided': result.get('recommendations_provided', False),
            'collected_info': result.get('collected_info', {})
        })
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the conversation"""
    
    try:
        if 'session_id' in session:
            session_id = session['session_id']
            if session_id in agents:
                agents[session_id].reset_conversation()
                print(f"\n🔄 RESET conversation for session: {session_id[:8]}...\n")
        
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


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get conversation statistics from logs"""
    
    try:
        if not os.path.exists('logs/conversations.jsonl'):
            return jsonify({
                'total_conversations': 0,
                'successful_matches': 0,
                'average_age': 0
            })
        
        with open('logs/conversations.jsonl', 'r') as f:
            logs = [json.loads(line) for line in f]
        
        total = len(logs)
        successful = sum(1 for log in logs if log.get('recommendations_provided'))
        
        ages = [log['collected_info'].get('age') for log in logs if log['collected_info'].get('age')]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        return jsonify({
            'total_conversations': total,
            'successful_matches': successful,
            'average_age': round(avg_age, 1),
            'success_rate': round(successful / total * 100, 1) if total > 0 else 0
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n" + "="*70)
        print("⚠️  WARNING: OpenAI API key not configured!")
        print("="*70)
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Get your key from: https://platform.openai.com/api-keys")
        print("\n" + "="*70 + "\n")
    
    print("\n" + "="*70)
    print("🚀 Starting AbilityPath Screening Agent (WITH LOGGING)")
    print("="*70)
    print("\n📊 Features enabled:")
    print("   ✅ Terminal logging - see every message")
    print("   ✅ File logging - conversations saved to logs/conversations.jsonl")
    print("   ✅ Statistics endpoint - GET /api/stats")
    print("\nAccess the web interface at: http://localhost:5001")
    print("Press Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
