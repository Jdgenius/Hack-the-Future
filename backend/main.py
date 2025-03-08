import os
import json
import google.api_core.exceptions
import google.generativeai as genai
import PIL.Image
from backend.receiver import receive_prompt
from backend.gemini_api import generate


def process_prompt(obj, file_name):
    """
    Processes the received prompt and image file.
    """

    # Get prompt data
    prompt_text = obj.get("Prompt", "Default analysis request.")

    # Ensure file path is correctly formatted
    file_path = os.path.abspath(file_name)  # Convert to absolute path

    # Validate image file
    if not os.path.exists(file_path):
        print(f"❌ Error: Image file not found at {file_path}")
        return None

    # Load image
    image = PIL.Image.open(file_path)

    # Call Gemini AI
    ai_response = generate(prompt_text, file_path)

    # Format response
    if ai_response:
        try:
            structured_response = json.loads(ai_response)  # Ensure valid JSON
        except json.JSONDecodeError:
            print("❌ Error: AI response is not valid JSON. Returning raw response.")
            structured_response = {"raw_response": ai_response}

        obj["Data"] = structured_response
        return obj
    else:
        return None


def send_response(original_object, response):
    return 

script_path = os.path.dirname(os.path.abspath(__file__))
testpath = os.path.join(script_path, "test.json")

with open(testpath, 'r') as file:
    data = json.load(file)

image_path = r"C:\Users\harin\OneDrive\HackTheFuture\Hack-the-Future\backend\images\bird.jpeg"

process_prompt(data, image_path)
