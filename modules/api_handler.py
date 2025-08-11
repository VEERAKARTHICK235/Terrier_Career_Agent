# modules/api_handler.py

import os
import requests
import json
import re  # Import the regular expression module
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key and construct the URL
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def get_llm_response(prompt: str) -> dict:
    """
    Sends a prompt to the Gemini API and returns a clean, parsed JSON dictionary.
    """
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data), timeout=60)
        response.raise_for_status()

        raw_text = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

        # Use regex to find a JSON object within the raw text. This is more robust.
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)

        if match:
            json_str = match.group(0)
            # Return the parsed dictionary
            return json.loads(json_str)
        else:
            print(f"ERROR: Could not find JSON in AI response: {raw_text}")
            return {"error": "AI response did not contain a valid JSON object."}

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return {"error": f"An API request error occurred: {e}"}
    except json.JSONDecodeError:
        print(f"JSON Decode Error. Raw text was: {raw_text}")
        return {"error": "Failed to decode the JSON object from the AI response."}
    except IndexError:
        print(f"Index Error. Full API response: {response.json()}")
        return {"error": "The API response format was unexpected."}