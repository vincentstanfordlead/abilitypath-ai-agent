# 🚀 Quick Start - 5 Minutes to Running Demo

## Step 1: Get Your OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

**Cost:** This demo uses GPT-3.5-turbo, which costs ~$0.002 per conversation. A full hackathon demo will cost less than $1.

## Step 2: Setup (1 minute)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env

# Edit .env and paste your API key
# On Mac/Linux: nano .env
# On Windows: notepad .env
# Replace: your_openai_api_key_here
# With: sk-your-actual-key
```

## Step 3: Run (30 seconds)

```bash
python web_app.py
```

You should see:
```
🚀 Starting AbilityPath Screening Agent
======================================
Access the web interface at: http://localhost:5002
```

## Step 4: Test (1 minute)

Open your browser to: **http://localhost:5002**

Try this conversation:
```
You: Hi, I need help for my 22-year-old son who just graduated high school

[Wait for response]

You: He needs daytime support while I work and we're hoping to find job training

[Wait for response]

You: What programs do you have?

[You should get program recommendations!]
```

## 🎉 That's it!

You now have a working AI screening agent!

---

## 📱 Testing Scenarios for Your Demo

### Scenario 1: Maria & Kevin (from the PDF)
```
"Hi, my son Kevin just turned 22 and graduated high school. 
I work full-time and need care for him during the day. 
I'm worried because I might have to quit my job if I can't find help soon."
```
**Should match:** Transition Services, Adult Day Program, Vocational Training

### Scenario 2: Early Intervention
```
"My 18-month-old daughter has developmental delays. 
Our pediatrician recommended early intervention services."
```
**Should match:** Early Intervention Services

### Scenario 3: Behavioral Support
```
"We need help with our 10-year-old son. He has autism and 
challenging behaviors. We need intensive support and respite 
care so we can get some rest."
```
**Should match:** Behavioral Services, Respite Care, School-Age Support

---

## 🐛 Quick Troubleshooting

### "Module not found" error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "OpenAI API key not configured"
- Check that `.env` file exists (not `.env.example`)
- Open `.env` and make sure your key is there
- Make sure there are no spaces: `OPENAI_API_KEY=sk-...`

### "Port 5002 already in use"
Edit `web_app.py`, change the last line from:
```python
app.run(debug=True, host='0.0.0.0', port=5002)
```
to:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then go to http://localhost:5001

### Chat not responding
1. Check your terminal for error messages
2. Verify internet connection
3. Check OpenAI API status: https://status.openai.com
4. Make sure your API key has available credits

---

## 🎯 What to Show in Your Hackathon Demo

### 1. The Problem (30 seconds)
- Show the PDF: "2-year wait times"
- Maria & Kevin's story

### 2. The Solution (2 minutes)
- Open the web interface
- Run through Maria & Kevin scenario
- Show instant program matches
- Highlight: "Tonight, not 2 years"

### 3. The Architecture (1 minute)
- Show the code structure
- Explain: Chat UI → AI Agent → Program Matching
- Mention: LangChain, OpenAI, Flask

### 4. Production Roadmap (1 minute)
- HIPAA compliance approach
- Scalability (handles 1,500+ weekly users)
- Easy maintenance (staff can update programs)
- Multi-channel (web, SMS, phone)

### 5. Impact (30 seconds)
- Instant screening vs. 2-year wait
- Staff focus on enrollment, not screening
- Better outcomes for families like Maria & Kevin

---

## 📊 Demo Tips

**DO:**
- ✅ Test your scenarios beforehand
- ✅ Have backup internet connection
- ✅ Show the web interface (looks professional)
- ✅ Explain how staff can update programs easily
- ✅ Emphasize the human-centered approach

**DON'T:**
- ❌ Don't show code during demo (unless asked)
- ❌ Don't get into technical details unless necessary
- ❌ Don't say "it's just a prototype" - say "MVP ready for pilot"
- ❌ Don't apologize for what it doesn't do - focus on what it does

---

## 🔧 Customizing for the Hackathon

### Add AbilityPath's Real Programs
Edit `programs_database.py`:
1. Find the `PROGRAMS` list
2. Replace with actual program details
3. Update eligibility criteria

### Change the AI's Personality
Edit `screening_agent.py`, line ~45:
```python
("system", """You are a warm, empathetic intake specialist...
```
Modify this text to match AbilityPath's brand voice.

### Update the Web Interface
Edit `templates/index.html`:
- Line 14-15: Update colors
- Line 53: Change title
- Line 54: Update tagline

---

## 💡 Advanced Features to Add (If Time)

### 1. Show Matching Logic Visually
Add to the chat response:
```
Why these programs match:
✓ Age: 22 years (matches Adult Day Program: 22-120)
✓ Needs daytime support (required for Adult Day Program)
✓ Seeking employment (matches Vocational Training)
```

### 2. Export Conversation Summary
Generate a PDF summary of the conversation and recommendations

### 3. Add Admin Panel
Simple page where staff can add/edit programs without coding

### 4. SMS Integration
Use Twilio to allow families to text with the agent

---

## 🎓 Understanding the Code (for Q&A)

**Q: How does it know what programs to recommend?**
A: The `filter_programs_by_criteria()` function in `programs_database.py` scores each program based on age and needs match. Programs with 60%+ match are recommended.

**Q: How does it extract information from conversation?**
A: The `extract_information()` method uses keyword matching. For production, we'd use more sophisticated NLP or train a custom model.

**Q: What if someone enters sensitive health information?**
A: For this demo, data stays in session memory. For production, we'd implement encryption, secure storage, and HIPAA compliance.

**Q: Can it handle multiple languages?**
A: Yes! OpenAI models support 50+ languages. Just change the system prompt to specify the language.

**Q: How would this scale to 1,500 users per week?**
A: Deploy on AWS Lambda or similar serverless platform. Each conversation is stateless. Use Redis for session management. Cost: ~$200-300/month at that scale.

---

## ✅ Pre-Hackathon Checklist

- [ ] OpenAI API key obtained and tested
- [ ] All Python packages installed
- [ ] Web interface runs successfully
- [ ] Tested all 3 demo scenarios
- [ ] Laptop charged + backup power
- [ ] Internet connection tested (+ hotspot backup)
- [ ] Presentation slides prepared
- [ ] Practiced 5-minute pitch
- [ ] Read through the README
- [ ] Understood the architecture

---

**You're ready! Good luck at the hackathon! 🚀**

Questions? Check the main README.md for detailed documentation.
