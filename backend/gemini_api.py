import base64
import os
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyBzIyq33V7Wwi4ke2b4Qf7xeqz01ON48LQ"

def generate(prompt_text, image_path):
    
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_text),
                types.Part.from_image(data=image_bytes),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_NONE",  # Block none
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_CIVIC_INTEGRITY",
                threshold="BLOCK_NONE",  # Block none
            ),
        ],
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Analyze the provided image of a returned product and generate a structured JSON output containing comprehensive insights. The output should be formatted for easy integration with a backend framework and displayed on a frontend dashboard. Assess the item based on the following criteria:

1. AI-Powered Defect Detection
Detect and classify physical defects such as:
Scratches
Tears
Dents
Missing parts
Malfunctions (if applicable)
Indicate severity of each detected defect on a scale from 1 to 10.
JSON Output Format Example:

json
Copy
Edit
\"defects\": {
    \"scratches\": {\"detected\": true, \"severity\": 6},
    \"tears\": {\"detected\": false, \"severity\": 0},
    \"dents\": {\"detected\": true, \"severity\": 3},
    \"missing_parts\": {\"detected\": false, \"severity\": 0},
    \"malfunction\": {\"detected\": false, \"severity\": 0}
}
2. Condition Grading System
Assign an overall quality score based on detected wear and tear:
\"Like New\" (Minor or no damage)
\"Used - Good\" (Visible wear but functional)
\"Used - Acceptable\" (Significant wear, some minor issues)
\"Salvage\" (Severe damage, non-functional)
JSON Output Format Example:

json
Copy
Edit
\"condition_grade\": \"Used - Good\"
3. AI for Counterfeit Detection
Compare product features, logos, branding, and serial numbers with known authentic items.
Determine likelihood of counterfeit (scale of 0-100%).
JSON Output Format Example:

json
Copy
Edit
\"counterfeit_detection\": {
    \"is_suspected_counterfeit\": false,
    \"confidence_score\": 8
}
4. Return Eligibility Checker
Check retailer's return policies against detected condition.
Recommend next steps:
\"Restock for resale\"
\"Repair before resale\"
\"Send to liquidation\"
\"Reject return\" (if counterfeit or severely damaged)
JSON Output Format Example:

json
Copy
Edit
\"return_eligibility\": {
    \"eligible\": true,
    \"recommended_action\": \"Repair before resale\"
}
5. Automated Repair & Refurbishment Recommendations
Suggest specific repair or refurbishment actions if applicable (e.g., replace missing parts, repaint, repackage).
Include estimated repair cost in USD.
JSON Output Format Example:

json
Copy
Edit
\"repair_recommendations\": {
    \"suggested_repairs\": [\"Repaint surface\", \"Replace missing button\"],
    \"estimated_cost_usd\": 15.50
}
6. Dynamic Discounting AI
Predict optimal resale price based on condition, demand, and market trends.
Provide a discount percentage based on original MSRP.
JSON Output Format Example:

json
Copy
Edit
\"dynamic_pricing\": {
    \"original_msrp\": 199.99,
    \"discounted_price\": 149.99,
    \"discount_percentage\": 25
}
7. Resale & Marketplace Integration
Identify best resale platform based on item type and demand:
Amazon
Walmart Liquidation
eBay
Poshmark
Direct auction to wholesalers
Determine auction viability (yes/no).
JSON Output Format Example:

json
Copy
Edit
\"resale_options\": {
    \"best_platform\": \"eBay\",
    \"auction_viable\": true
}
Final Structured JSON Output Example:
json
Copy
Edit
{
    \"defects\": {
        \"scratches\": {\"detected\": true, \"severity\": 6},
        \"tears\": {\"detected\": false, \"severity\": 0},
        \"dents\": {\"detected\": true, \"severity\": 3},
        \"missing_parts\": {\"detected\": false, \"severity\": 0},
        \"malfunction\": {\"detected\": false, \"severity\": 0}
    },
    \"condition_grade\": \"Used - Good\",
    \"counterfeit_detection\": {
        \"is_suspected_counterfeit\": false,
        \"confidence_score\": 8
    },
    \"return_eligibility\": {
        \"eligible\": true,
        \"recommended_action\": \"Repair before resale\"
    },
    \"repair_recommendations\": {
        \"suggested_repairs\": [\"Repaint surface\", \"Replace missing button\"],
        \"estimated_cost_usd\": 15.50
    },
    \"dynamic_pricing\": {
        \"original_msrp\": 199.99,
        \"discounted_price\": 149.99,
        \"discount_percentage\": 25
    },
    \"resale_options\": {
        \"best_platform\": \"eBay\",
        \"auction_viable\": true
    }
}"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
