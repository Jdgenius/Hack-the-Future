import os
import json
import base64
import google.api_core.exceptions
import google.generativeai as genai


import PIL.Image

def call_gemini(prompt, image):
    try:
        generation_config = genai.GenerationConfig(
            temperature=1,  
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,       
            
            response_mime_type="text/plain",

        )

        model = genai.GenerativeModel("gemini-2.0-flash")
        
        response = model.generate_content([prompt, image], generation_config=generation_config)
        response_list = response.text
        return response_list

    except FileNotFoundError:
        print(f"Error: Image file not found at {filepath}")
        return None
    except google.api_core.exceptions.GoogleAPIError as e:
        print(f"Error calling Gemini API: {e}")
        return None
    except Exception as generic_exception:
        print(f"An unexpected error occurred: {generic_exception}")
        return None 



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

    #Finding List of Materials

    genai.configure(api_key="GEMINI_AI_KEY")

    response_list = call_gemini(prompt, image)
    
    #Processing Model Output
    response_lists = response_list.split(',')
    string_list = [s.strip() for s in response_lists]
    print(string_list)

    #Finding recyclability (and percentage)
    parameter_prompt = "Output a one-line no semicolon comma separated list containing the recyclability percentage of the packaging, and 'recyclable' or 'not recyclable' if packaging is recyclable or not. refer to US laws to determine recyclability, here's some data about the packaging's raw materials:"
    parameter_prompt = parameter_prompt + response_list

    resp = call_gemini(parameter_prompt, image)
    resp_list = resp.split(',')
    list = [s.strip() for s in resp_list]
    print(list)

    #Format response into a object and return the object
    obj["Data"] = response_list

    return obj

def send_response(original_object, response):
    return 

script_path = os.path.dirname(os.path.abspath(__file__))
testpath = os.path.join(script_path, "test.json")
with open(testpath, 'r') as file:
    data = json.load(file)

process_prompt(data, "s-l1200.jpeg")