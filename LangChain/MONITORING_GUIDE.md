# 🔍 Monitoring & Evaluation Guide

This guide shows you how to see what your AI agent is doing and evaluate its performance.

---

## 🎯 **Quick Answer: 4 Ways to Monitor**

1. **Terminal Logs** - See what's happening in real-time (easiest!)
2. **Add Debug Print Statements** - Track specific variables
3. **LangChain Verbose Mode** - See the AI's thought process
4. **LangSmith** - Professional monitoring (recommended for production)

---

## 1️⃣ **TERMINAL LOGS (Easiest - Start Here!)**

### **What You See Now:**

When you run `python3 web_app.py`, you see:
```
🚀 Starting AbilityPath Screening Agent
======================================
Access the web interface at: http://localhost:5001
```

But you're NOT seeing what's happening during conversations!

### **Enable Basic Logging:**

**Option A: See HTTP Requests**

The Flask server already shows basic logs. You should see:
```
127.0.0.1 - - [05/Nov/2024 12:34:56] "POST /api/chat HTTP/1.1" 200 -
```

This tells you:
- When a message was sent
- If it succeeded (200) or failed (400/500)

**Option B: Add Custom Logging**

Edit `web_app.py` and add logging:

**Find this section (around line 48):**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(16)
        
        session_id = session['session_id']
        
        # Get user message
        data = request.json
        user_message = data.get('message', '')
```

**Add these print statements:**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = secrets.token_hex(16)
        
        session_id = session['session_id']
        
        # Get user message
        data = request.json
        user_message = data.get('message', '')
        
        # 🔍 ADD THESE LINES:
        print("\n" + "="*60)
        print(f"📨 NEW MESSAGE from session: {session_id[:8]}...")
        print(f"👤 User: {user_message}")
        print("="*60)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get agent and process message
        agent = get_agent(session_id)
        result = agent.chat(user_message)
        
        # 🔍 ADD THESE LINES:
        print(f"🤖 Agent: {result['response'][:100]}...")  # First 100 chars
        print(f"📊 Collected Info: {result.get('collected_info', {})}")
        print(f"✅ Recommendations provided: {result.get('recommendations_provided', False)}")
        print("="*60 + "\n")
```

Now when you run the server, you'll see:
```
============================================================
📨 NEW MESSAGE from session: a1b2c3d4...
👤 User: Hi, my son Kevin is 22 and just graduated
============================================================
🤖 Agent: I'm so glad you reached out! I understand how str...
📊 Collected Info: {'name': None, 'age': 22, 'needs': {'recently_graduated': True}}
✅ Recommendations provided: False
============================================================
```

---

## 2️⃣ **ADD DEBUG PRINT STATEMENTS**

### **Track What Information is Being Extracted**

Edit `screening_agent.py` to see what's happening inside the agent.

**Find the `extract_information` method (around line 85):**

Add print statements to see what's being extracted:

```python
def extract_information(self, user_message, ai_response):
    """Extract structured information from the conversation"""
    
    user_lower = user_message.lower()
    
    # 🔍 ADD THIS:
    print(f"\n🔍 EXTRACTING from: '{user_message}'")
    
    # Extract age
    if "year" in user_lower or "age" in user_lower:
        words = user_message.split()
        for i, word in enumerate(words):
            if word.isdigit():
                age = int(word)
                if 0 <= age <= 120:
                    self.collected_info["age"] = age
                    print(f"   ✅ Extracted AGE: {age}")  # 🔍 ADD THIS
                    break
    
    # Extract needs based on keywords
    needs_keywords = {
        "developmental_delay": ["delay", "delayed", "behind", "developmental"],
        # ... rest of keywords ...
    }
    
    # 🔍 ADD THIS:
    extracted_needs = []
    
    for need, keywords in needs_keywords.items():
        if any(keyword in user_lower for keyword in keywords):
            self.collected_info["needs"][need] = True
            extracted_needs.append(need)  # 🔍 ADD THIS
    
    # 🔍 ADD THIS:
    if extracted_needs:
        print(f"   ✅ Extracted NEEDS: {', '.join(extracted_needs)}")
    print(f"   📊 Total info collected: Age={self.collected_info['age']}, Needs count={len(self.collected_info['needs'])}\n")
```

**Now you'll see:**
```
🔍 EXTRACTING from: 'Hi, my son Kevin is 22 and needs job training'
   ✅ Extracted AGE: 22
   ✅ Extracted NEEDS: recently_graduated, seeking_employment
   📊 Total info collected: Age=22, Needs count=2
```

---

## 3️⃣ **LANGCHAIN VERBOSE MODE (See AI Thinking)**

### **Enable LangChain's Built-in Debugging**

Edit `screening_agent.py` around line 150:

**Find this:**
```python
conversation = LLMChain(
    llm=self.llm,
    prompt=prompt,
    memory=self.memory,
    verbose=False  # <-- Currently False
)
```

**Change to:**
```python
conversation = LLMChain(
    llm=self.llm,
    prompt=prompt,
    memory=self.memory,
    verbose=True  # <-- Changed to True!
)
```

**Now you'll see the full LangChain trace:**
```
> Entering new LLMChain chain...
Prompt after formatting:
System: You are a warm, empathetic intake specialist...
Human: Hi, my son is 22 and needs help

> Finished chain.
```

This shows:
- The exact prompt sent to OpenAI
- The conversation history
- The AI's response
- Token usage

---

## 4️⃣ **LANGSMITH - Professional Monitoring (Best for Production)**

### **What is LangSmith?**
- Official monitoring platform from LangChain creators
- Tracks all conversations, prompts, responses
- Shows token usage and costs
- Allows A/B testing different prompts
- **FREE tier available!**

### **Setup (5 minutes):**

**Step 1: Sign up**
Go to: https://smith.langchain.com/

**Step 2: Get your API key**
- Click on your profile
- Go to "API Keys"
- Create new key

**Step 3: Add to your .env file**
```bash
# Add these lines to your .env file:
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=abilitypath-screening-agent
```

**Step 4: Install the package**
```bash
pip3 install langsmith
```

**Step 5: Restart your server**
```bash
python3 web_app.py
```

**Step 6: View traces**
Go to: https://smith.langchain.com/
- You'll see every conversation
- Click on any to see full trace
- See exact prompts, responses, timing

### **What You Get:**

**Dashboard shows:**
- 📊 Total conversations
- ⏱️ Average response time
- 💰 Token usage & costs
- ⚠️ Error rate
- 📈 Performance trends

**Per-conversation trace:**
- Full conversation history
- Exact prompts sent to OpenAI
- AI responses
- Information extracted
- Programs matched
- Timing breakdown

---

## 5️⃣ **SAVE CONVERSATIONS TO FILE (Simple Logging)**

### **Log Every Conversation**

Add this to `web_app.py`:

**At the top, add:**
```python
import json
from datetime import datetime
```

**In the `/api/chat` endpoint, add:**
```python
# After getting the result
result = agent.chat(user_message)

# 🔍 ADD THIS - Log to file
log_entry = {
    "timestamp": datetime.now().isoformat(),
    "session_id": session_id,
    "user_message": user_message,
    "agent_response": result['response'],
    "collected_info": result.get('collected_info', {}),
    "recommendations_provided": result.get('recommendations_provided', False)
}

with open('conversation_logs.jsonl', 'a') as f:
    f.write(json.dumps(log_entry) + '\n')
```

**Now every conversation is saved to `conversation_logs.jsonl`**

You can analyze it later with:
```python
import json

# Read all conversations
with open('conversation_logs.jsonl', 'r') as f:
    conversations = [json.loads(line) for line in f]

# Count total conversations
print(f"Total conversations: {len(conversations)}")

# Count successful matches
successful = sum(1 for c in conversations if c['recommendations_provided'])
print(f"Successful matches: {successful}")

# Average age of clients
ages = [c['collected_info'].get('age') for c in conversations if c['collected_info'].get('age')]
print(f"Average age: {sum(ages)/len(ages):.1f}")
```

---

## 6️⃣ **CREATE A SIMPLE EVALUATION SCRIPT**

Create a new file: `evaluate_agent.py`

```python
"""
Simple evaluation script to test agent performance
"""

from screening_agent import ScreeningAgent
import os
from dotenv import load_dotenv

load_dotenv()

# Test cases with expected results
test_cases = [
    {
        "name": "Maria & Kevin",
        "messages": [
            "Hi, my son Kevin is 22 and just graduated high school.",
            "He needs daytime support while I work and job training.",
            "What programs can help?"
        ],
        "expected_age": 22,
        "expected_needs": ["recently_graduated", "needs_daytime_support", "seeking_employment"],
        "expected_programs": ["transition_services", "adult_day_program", "vocational_training"]
    },
    {
        "name": "Early Intervention",
        "messages": [
            "My 2-year-old daughter has developmental delays.",
            "What early intervention services do you have?"
        ],
        "expected_age": 2,
        "expected_needs": ["developmental_delay"],
        "expected_programs": ["early_intervention"]
    },
    # Add more test cases...
]

def run_evaluation():
    api_key = os.getenv("OPENAI_API_KEY")
    
    results = []
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test['name']}")
        print('='*60)
        
        agent = ScreeningAgent(api_key)
        
        # Run through messages
        for msg in test['messages']:
            print(f"\n👤 User: {msg}")
            result = agent.chat(msg)
            print(f"🤖 Agent: {result['response'][:100]}...")
        
        # Check results
        collected_info = agent.collected_info
        
        # Evaluate
        evaluation = {
            "test_name": test['name'],
            "age_correct": collected_info['age'] == test['expected_age'],
            "needs_extracted": len(collected_info['needs']),
            "expected_needs": len(test['expected_needs']),
            "passed": True  # We'll determine this
        }
        
        print(f"\n📊 Evaluation:")
        print(f"   Age extracted: {collected_info['age']} (expected: {test['expected_age']})")
        print(f"   Needs extracted: {list(collected_info['needs'].keys())}")
        print(f"   Expected needs: {test['expected_needs']}")
        print(f"   ✅ Age correct: {evaluation['age_correct']}")
        
        results.append(evaluation)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    passed = sum(1 for r in results if r['age_correct'])
    print(f"Age extraction: {passed}/{len(results)} correct")
    
if __name__ == "__main__":
    run_evaluation()
```

**Run it:**
```bash
python3 evaluate_agent.py
```

---

## 📊 **COMPARISON: Which Method to Use?**

| Method | Difficulty | Information | Best For |
|--------|-----------|-------------|----------|
| Terminal logs | Easy | Basic | Quick debugging |
| Print statements | Easy | Custom | Specific issues |
| LangChain verbose | Easy | Detailed | Understanding AI flow |
| LangSmith | Medium | Complete | Production monitoring |
| Log files | Easy | Historical | Analysis later |
| Eval script | Medium | Systematic | Testing changes |

---

## 🎯 **RECOMMENDED APPROACH FOR HACKATHON**

### **For Development (Now):**
1. ✅ Add print statements to `web_app.py` (see terminal logs)
2. ✅ Enable `verbose=True` in LangChain (see AI thinking)
3. ✅ Watch terminal while testing

### **For Hackathon Demo:**
1. ✅ Turn off verbose mode (cleaner output)
2. ✅ Keep basic logging (monitor for errors)
3. ✅ Have eval script ready to show testing

### **For Production (Later):**
1. ✅ Use LangSmith for full monitoring
2. ✅ Save conversations to database
3. ✅ Build analytics dashboard

---

## ⚡ **QUICK START: See Traces Now**

Run these commands RIGHT NOW:

**Step 1: Edit web_app.py**
Add the print statements from section 1

**Step 2: Edit screening_agent.py**
Change `verbose=False` to `verbose=True` (line ~150)

**Step 3: Restart server**
```bash
# Stop: Ctrl + C
python3 web_app.py
```

**Step 4: Test a conversation**
Open browser, send a message

**Step 5: Watch your terminal!**
You'll see everything happening in real-time!

---

## 🔍 **EXAMPLE: What You'll See**

**In terminal after adding logging:**

```
============================================================
📨 NEW MESSAGE from session: a1b2c3d4...
👤 User: Hi, my son is 22 and needs job training
============================================================

🔍 EXTRACTING from: 'Hi, my son is 22 and needs job training'
   ✅ Extracted AGE: 22
   ✅ Extracted NEEDS: recently_graduated, seeking_employment
   📊 Total info collected: Age=22, Needs count=2

> Entering new LLMChain chain...
Prompt after formatting:
System: You are a warm, empathetic intake specialist for AbilityPath...
Human: Hi, my son is 22 and needs job training

> Finished chain.

🤖 Agent: I'm so glad you reached out. It sounds like Kevin is...
📊 Collected Info: {'name': None, 'age': 22, 'needs': {'recently_graduated': True, 'seeking_employment': True}}
✅ Recommendations provided: False
============================================================
```

**This tells you:**
- ✅ What user said
- ✅ What age was extracted
- ✅ What needs were identified
- ✅ What prompt was sent to OpenAI
- ✅ What response came back
- ✅ Whether recommendations were given

---

## 💡 **PRO TIP: Color-Code Your Logs**

Make logs easier to read with colors:

```bash
pip3 install colorama
```

Then in your code:
```python
from colorama import Fore, Style

print(f"{Fore.GREEN}✅ Extracted AGE: {age}{Style.RESET_ALL}")
print(f"{Fore.BLUE}🤖 Agent: {response}{Style.RESET_ALL}")
print(f"{Fore.RED}❌ Error: {error}{Style.RESET_ALL}")
```

---

## ✅ **ACTION ITEMS FOR YOU**

1. **Right now:** Add print statements to `web_app.py`
2. **Right now:** Enable `verbose=True` in `screening_agent.py`
3. **Restart server** and test
4. **Watch terminal** to see everything happening
5. **Later:** Sign up for LangSmith for professional monitoring

---

**Want me to help you add the logging code right now? I can show you exactly which lines to add!** 🚀
