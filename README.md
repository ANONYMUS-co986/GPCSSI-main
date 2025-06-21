# Cybercrime Intelligence Assistant (Python)

This is a powerful, web-based AI chatbot for cybercrime intelligence, built in Python. It is designed to be a serious tool, not a demo.

## Features

- **True AI Chatbot**: Runs in your browser with a modern, responsive interface
- **Strict Logic Cascade**: The bot has its own "brain" and follows a precise order to get answers:
    1.  **Internal Knowledge**: Answers common questions (e.g., "what is malware?") instantly from its built-in knowledge base.
    2.  **Local Datasets**: If the question is not in its knowledge base, it intelligently searches the `cybercrimedata.csv` and `cybersecurity_attacks.csv` files for specific entities.
    3.  **Gemini API Fallback**: Only as a final resort, if it finds no answers internally or in the local files, will it query the Google Gemini API.
- **Sarcasm Mode**: A fully functional sarcasm mode that changes the bot's personality for witty, snarky responses.
- **Conversation Memory**: The bot remembers the context of your conversation for intelligent follow-up questions.
- **Clean & Professional**: No gimmicks. Just a powerful, functional tool for intelligence gathering.

## Setup

### 1. Prerequisites
- You must have Python 3.x installed on your system.

### 2. Install Dependencies
Open your terminal or command prompt and run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Set Up Your Gemini API Key (Required)
The chatbot requires a Google Gemini API key to function properly. Follow these steps:

1. Get your API key from Google AI Studio (https://makersuite.google.com/app/apikey)
2. Set the environment variable before running the application:

   **Windows (Command Prompt)**:
   ```cmd
   set GEMINI_API_KEY=your-api-key-here
   ```

   **Windows (PowerShell)**:
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```

   **Linux/macOS**:
   ```bash
   export GEMINI_API_KEY=your-api-key-here
   ```

   **Important Notes**: 
   - Replace `your-api-key-here` with your actual Gemini API key
   - For permanent setup, add the export command to your `~/.bashrc`, `~/.zshrc`, or equivalent
   - Make sure to restart your terminal after setting the environment variable

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the directory where you saved these files.
3. Run the web application with:
   ```bash
   python app.py
   ```
4. Open your browser and go to: `http://localhost:5000`

## How to Use the Chatbot

Simply type your question in the chat interface and press Enter or click Send.

### Special Commands

- `/sarcasm`: Type this to toggle sarcasm mode on or off. The bot will confirm the change.
- `/clear`: Type this to clear the current conversation history and start fresh.
- `/quit` or `/exit`: Type this to shut down the chatbot.

### Example Questions

- **To use internal knowledge**: `what is phishing?`
- **To search local data**: `tell me about the Adobe breach`
- **To use the Gemini API**: `what was the most common attack vector in 2022?`

### Troubleshooting

If you get errors about the API not working:
1. Make sure you've set the GEMINI_API_KEY environment variable correctly
2. Verify your API key is valid
3. Try opening a new terminal window after setting the environment variable
4. Check the console output for specific error messages 