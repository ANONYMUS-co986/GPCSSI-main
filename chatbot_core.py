import google.generativeai as genai
from colorama import init, Fore, Style
import os
import time
from datetime import datetime, timedelta

# Configure Gemini API
genai.configure(api_key="AIzaSyAll7KiDZyYf3tEUOpgq8BW-AU9SYtNT1A")

# Create model using a lighter version
MODEL_NAME = "models/gemini-2.0-flash-lite"
print(f"\nInitializing with model: {MODEL_NAME}")

class RateLimiter:
    def __init__(self, max_requests_per_minute=10):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        now = datetime.now()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < timedelta(minutes=1)]
        
        if len(self.requests) >= self.max_requests:
            # Wait until oldest request is more than 1 minute old
            sleep_time = 61 - (now - self.requests[0]).total_seconds()
            if sleep_time > 0:
                print(f"Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            self.requests = self.requests[1:]
        
        self.requests.append(now)

rate_limiter = RateLimiter(max_requests_per_minute=5)

try:
    model = genai.GenerativeModel(MODEL_NAME)
    print("Successfully created model")
except Exception as e:
    print(f"Error creating model: {e}")
    raise Exception("Could not initialize model")

class CybercrimeChatbot:
    def __init__(self):
        self.is_sarcasm_enabled = False
        print("Initializing chatbot...")
        try:
            # Test API connection with minimal prompt
            rate_limiter.wait_if_needed()
            response = model.generate_content("Test", safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ])
            print("API connection successful!")
        except Exception as e:
            print(f"Error testing API: {e}")

    def get_response(self, query):
        # First check if it's a command
        command_response = self._handle_command(query.lower().strip())
        if command_response:
            return command_response

        # Check for creator question
        query_lower = query.lower().strip()
        if any(phrase in query_lower for phrase in ["who made you", "who created you", "who developed you", "who built you", "who is your creator", "who's your creator"]):
            return "I was created by ANUJ PHULERA (CA 44) from GPCSSI using python,html and css"

        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Wait if needed before making the request
                rate_limiter.wait_if_needed()
                
                # Add context to the query
                prompt = f"""You are a cybersecurity expert assistant. Please answer the following question:
                Question: {query}
                
                If the question is about a person, provide information about their role in cybersecurity if relevant.
                If the question is about a cyber attack or breach, provide details about what happened.
                If the question is about a cybersecurity concept, explain it clearly.
                
                {'Please respond in a sarcastic, witty tone while still being informative.' if self.is_sarcasm_enabled else 'Please respond in a professional, informative tone.'}
                """
                
                print(f"Sending query to API (attempt {retry_count + 1}/{max_retries})")
                response = model.generate_content(prompt, safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ])
                print("Received response from API")
                
                if response and response.text:
                    return response.text.strip()
                else:
                    print("Empty response from API")
                    retry_count += 1
                    time.sleep(2 ** retry_count)  # Exponential backoff
                    
            except Exception as e:
                print(f"Error in get_response (attempt {retry_count + 1}/{max_retries}): {str(e)}")
                if "quota" in str(e).lower():
                    return "I'm currently experiencing high demand and have reached my quota limit. Please try again in a few minutes."
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2 ** retry_count)  # Exponential backoff
                else:
                    return f"I encountered an error after {max_retries} attempts. Please try again later."
        
        return "I'm having trouble generating a response. Please try again."

    def _handle_command(self, command):
        if command == "/sarcasm":
            self.is_sarcasm_enabled = not self.is_sarcasm_enabled
            return f"Sarcasm mode is now {'enabled' if self.is_sarcasm_enabled else 'disabled'}."
        elif command == "/clear":
            return "Conversation history cleared."
        elif command in ["/quit", "/exit"]:
            return "exit"
        return None