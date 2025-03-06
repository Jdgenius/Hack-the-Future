import os
import json
import base64
import google.api_core.exceptions
import google.generativeai as genai


import PIL.Image

def receive_prompt():
    #Block until Figma API sends data over, and receive the prompt data (and an image if there is one)
    return 

def process_prompt(obj, File):

    #Reading data from sent object
    type = obj["Type"]
    
    prompt = obj["Prompt"]
   

    #Fetching path of image
    script_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_path, "images", File)

    image = PIL.Image.open(filepath)

    #Processing Prompt

    #Sending to Gemini

    genai.configure(api_key="AIzaSyDAPW9X8Sp6Si6Um0fW7INNkpdvdPc88ps")

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([prompt, image])
        print(response.text)

    except FileNotFoundError:
        print(f"Error: Image file not found at {filepath}")
        return None
    except google.api_core.exceptions.GoogleAPIError as e:
        print(f"Error calling Gemini API: {e}")
        return None
    except Exception as generic_exception:
        print(f"An unexpected error occurred: {generic_exception}")
        return None 
    
    

    #Format response into a object and return the object
    obj["Data"] = response.text

    return obj

def send_response(original_object, response):
    return 

script_path = os.path.dirname(os.path.abspath(__file__))
testpath = os.path.join(script_path, "test.json")
with open(testpath, 'r') as file:
    data = json.load(file)

process_prompt(data, "bird.jpeg")
