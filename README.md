🌍 Multilingual AI Chatbot

Build your own ChatGPT-style chatbot in under 15 minutes! Supports 8+ languages and runs completely FREE.

Perfect for demos, experiments, or multilingual support in your projects.

✨ Features

🌐 8+ Languages: English, Spanish, French, German, Hindi, Japanese, Chinese, Arabic
💬 Multiple Chat Histories: Keep separate conversations
⚡ Lightning Fast: Powered by Groq API
💰 100% Free – no hidden costs
🎨 Customizable AI Personality – tweak system messages for your style

🚀 Quick Start
1. Clone & Install
git clone https://github.com/yourusername/multilingual-chatbot.git
cd multilingual-chatbot
pip install groq streamlit

2. Get Your API Key

Go to Groq Console
Sign up (FREE, no credit card)
Create an API key
Copy it

3. Add Your Key

Never hardcode API keys in source files.
Locally (PowerShell):
$env:GROQ_API_KEY = "paste_your_key_here"
streamlit run ui.py

Streamlit Cloud / Hosting:
Set a secret/environment variable named GROQ_API_KEY in your deployment environment.
Local .streamlit/secrets.toml example:

# .streamlit/secrets.toml
GROQ_API_KEY = "paste_your_key_here"


The app will automatically use the environment variable or st.secrets at runtime.

4. Run the App
streamlit run ui.py


Open http://localhost:8501
 in your browser and start chatting.

📁 Files
backend.py  → AI logic and language handling
ui.py       → User interface (Streamlit)

🎨 Customization Tips

Add languages: Edit the languages list in ui.py
Change AI personality: Modify the system_message in backend.py
Swap models: For faster responses, try llama-3.1-8b-instant. For high-fidelity, use llama-3.3-70b-versatile

🐛 Common Issues

Module not found: pip install groq streamlit
Invalid API key: Double-check your Groq console key
Model error: Switch to a different model (llama-3.3-70b-versatile)