# AbilityPath AI Assistant

## Introduction
This repository hosts two interconnected projects that together power the **AbilityPath AI Assistant**, an intelligent chatbot designed to provide accessible support and information for AbilityPath users.

1. **LangChain Project** — a full-stack implementation using LangChain for language model orchestration, including the frontend, backend, and model pipeline.
2. **Dialogflow Project** — a workflow and chat system powered by Dialogflow Playbook and chart logic, including a deployable web widget for integration into the AbilityPath website.

---

## Summary

### **LangChain Folder**
This folder contains:
- **Frontend**: User interface built to interact with the AI assistant.
- **Backend**: API routes and logic that communicate with the model.
- **Model**: LangChain pipelines for prompt management, data retrieval, and response generation.

The LangChain project enables dynamic, context-aware responses using LLMs and custom knowledge bases.

### **Dialogflow Folder**
This folder includes:
- **Playbook**: A Dialogflow-based conversational flow that guides users through structured dialogues.
- **Charts**: Visual representations and logical flows for conversation management.
- **`widget.html`**: A standalone HTML file that embeds the Dialogflow chatbox widget into any webpage.

To add the chat widget to **[abilitypath.org](https://abilitypath.org/)** or another site, simply insert the content of `widget.html` into the site’s HTML file before the closing `</body>` tag.  
This will render a floating chat bubble titled **“Abby – AbilityPath AI”**.

---

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- npm or yarn
- Access to a Dialogflow agent and a Google Cloud project
- Optional: Firebase for hosting or database integration

### Setup for **LangChain Project**
```bash
cd LangChain
npm install           # install frontend dependencies
pip install -r requirements.txt   # install backend dependencies
npm run dev           # start frontend (if React/Vue)
python app.py         # or uvicorn main:app --reload
```

### Setup for **Dialogflow Project**
```bash
cd Diagramflow
# Edit playbook or chart as needed using the Dialogflow console
# Upload or sync updated flow files here
```

### Test the Widget Locally
1. Open `Diagramflow/widget.html` in a browser.
2. You should see a floating chat bubble labeled **“Abby – AbilityPath AI.”**
3. To test it on your site, paste the contents of `widget.html` into the `<body>` section of your site’s HTML file.

---

## Q & A

**Q: What’s the difference between LangChain and Dialogflow projects?**  
A: LangChain handles advanced reasoning and model orchestration, while Dialogflow provides rule-based conversation flows and visual playbook tools.

**Q: How do I update the chat flow?**  
A: Modify the playbook or chart inside the `Diagramflow` folder and re-export from Dialogflow if necessary.

**Q: Can I host the chatbot widget elsewhere?**  
A: Yes. Copy the contents of `widget.html` into any website. Just ensure the correct `project-id` and `agent-id` values remain in place.

**Q: Does the LangChain backend connect to Dialogflow?**  
A: Not directly — they’re complementary approaches. You can extend the LangChain backend to integrate Dialogflow API calls if needed.
