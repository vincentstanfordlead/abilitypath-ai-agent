# 🎯 START HERE - Access Your Demo

## 📍 Your Demo Location

Your complete working prototype is in:
```
/home/user/abilitypath_prototype/
```

## 🚀 3 Ways to Access Your Demo

### Option 1: Download to Your Computer (RECOMMENDED)

Since you're in a cloud environment, you need to download the files to your local computer to run the demo.

**Steps:**
1. In your file browser (left sidebar), navigate to: `/home/user/abilitypath_prototype/`
2. Right-click on the `abilitypath_prototype` folder
3. Select "Download" or "Download as ZIP"
4. Extract the files on your local computer
5. Follow the instructions below

### Option 2: Use AI Drive Tool

I can help you copy all files to your AI Drive for easy access:

Let me know if you want me to do this!

### Option 3: Run in This Environment (If Supported)

If this environment allows running web servers, you can run it here.

---

## 💻 How to Run the Demo (On Your Local Computer)

### Step 1: Open Terminal/Command Prompt
- **Windows:** Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux:** Press `Cmd + Space`, type `terminal`, press Enter

### Step 2: Navigate to the Folder
```bash
cd /path/to/abilitypath_prototype
```
(Replace `/path/to/` with wherever you extracted the files)

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Your API Key
```bash
# Create .env file from example
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Windows: notepad .env
# Mac: nano .env
# Linux: nano .env
```

**Get your API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign up/login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)
5. Paste it in the .env file

### Step 5: Verify Everything is Set Up
```bash
python verify_setup.py
```

This will check:
- ✅ Python version
- ✅ All packages installed
- ✅ API key configured
- ✅ Files in place
- ✅ OpenAI connection works

### Step 6: Run the Demo!
```bash
python web_app.py
```

You should see:
```
🚀 Starting AbilityPath Screening Agent
======================================
Access the web interface at: http://localhost:5002
```

### Step 7: Open Your Browser
Go to: **http://localhost:5002**

---

## 🎬 Demo It!

Once the web page opens, try this conversation:

**Message 1:**
```
Hi, I'm Maria. My son Kevin just turned 22 and graduated from high school. 
I need to find daytime care for him within 30 days or I'll have to quit my job.
```

**Wait for AI response, then Message 2:**
```
He needs daytime support while I work and we're hoping to find job training too. 
What programs can help us?
```

**You should get program recommendations!**

---

## 📁 What's in Each File

### 🎯 Essential Files to Understand:

**`programs_database.py`** - The program definitions
- Contains 10 sample programs
- Eligibility criteria for each
- Matching algorithm that scores programs

**`screening_agent.py`** - The AI brain
- Uses LangChain to manage conversations
- Extracts age and needs from dialogue
- Decides when to show recommendations

**`web_app.py`** - The web server
- Flask API with 3 endpoints
- `/api/chat` - send messages
- `/api/reset` - start new conversation
- `/api/status` - check if API key is set

**`templates/index.html`** - The chat interface
- Beautiful, responsive design
- Real-time chat experience
- No external dependencies

### 📚 Documentation Files:

**`README.md`** - Complete overview and setup
**`QUICKSTART.md`** - 5-minute fast start guide
**`HACKATHON_GUIDE.md`** - Presentation tips
**`test_scenarios.txt`** - Test cases for demo

### ⚙️ Configuration Files:

**`requirements.txt`** - Python packages needed
**`.env.example`** - Template for API key
**`verify_setup.py`** - Automated setup checker

---

## 🎥 Alternative: View Files in Browser

You can view/download individual files by clicking these links:

- [View README.md](computer:///home/user/abilitypath_prototype/README.md)
- [View QUICKSTART.md](computer:///home/user/abilitypath_prototype/QUICKSTART.md)
- [View programs_database.py](computer:///home/user/abilitypath_prototype/programs_database.py)
- [View screening_agent.py](computer:///home/user/abilitypath_prototype/screening_agent.py)
- [View web_app.py](computer:///home/user/abilitypath_prototype/web_app.py)
- [View test_scenarios.txt](computer:///home/user/abilitypath_prototype/test_scenarios.txt)

---

## ❓ Common Questions

**Q: I don't have Python on my computer. What do I do?**
A: Download Python from https://www.python.org/downloads/ (version 3.8 or higher)

**Q: How much does the OpenAI API cost?**
A: GPT-3.5-turbo costs about $0.002 per conversation. A full demo day costs less than $1.

**Q: Can I run this without downloading?**
A: You need to run it on a computer with Python. Cloud environments usually don't allow web servers.

**Q: What if I get errors?**
A: Run `python verify_setup.py` - it will tell you exactly what's wrong and how to fix it.

**Q: Can I modify the code?**
A: Absolutely! That's the point. Edit `programs_database.py` to add your real programs.

---

## 🆘 Need Help?

### Quick Troubleshooting:

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"OpenAI API key not configured"**
- Edit `.env` file
- Make sure it says: `OPENAI_API_KEY=sk-your-key-here`
- No spaces, no quotes

**"Port 5002 already in use"**
- Edit `web_app.py`, change last line to: `app.run(debug=True, port=5001)`
- Then go to http://localhost:5001

**"Can't connect to OpenAI"**
- Check internet connection
- Verify API key is correct
- Check if you have API credits: https://platform.openai.com/account/usage

---

## 🎯 What to Do Next

1. **Download the files** to your local computer
2. **Follow the setup steps** above (takes 5 minutes)
3. **Run the demo** and test it with Maria & Kevin scenario
4. **Read the documentation** to understand how it works
5. **Practice your pitch** using HACKATHON_GUIDE.md

---

## 💡 Quick Tips

- **Test it before the hackathon** - make sure everything works
- **Have a backup plan** - take screenshots/video in case of internet issues
- **Know your code** - be able to explain each file's purpose
- **Customize it** - add AbilityPath's real programs if you have them
- **Practice the demo** - do it 3-5 times so it's smooth

---

## 🎉 You're All Set!

Your complete AI screening agent prototype is ready. Just download it, set up your API key, and run it!

**Everything you need is in this folder.**

Good luck! 🚀
