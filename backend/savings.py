import os
import json
import google.generativeai as genai
import time
import re

# Configure AI Model (Use the latest working model)
genai.configure(api_key="AIzaSyDAPW9X8Sp6Si6Um0fW7INNkpdvdPc88ps")

# Define Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RETURNS_JSON_PATH = os.path.join(SCRIPT_DIR, "returns.json")
OUTPUT_JSON_PATH = os.path.join(SCRIPT_DIR, "savings_analysis.json")

def call_ai_model(prompt):
    """
    Calls the AI model with a given prompt and retrieves the response.
    """
    try:
        generation_config = genai.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=512,
            response_mime_type="text/plain"
        )

        model = genai.GenerativeModel("gemini-1.5-pro-latest")  
        response = model.generate_content([prompt], generation_config=generation_config)
        return response.text.strip()

    except Exception as e:
        print(f"AI Model Error: {e}")
        return "AI estimation failed"

def extract_savings_from_ai_response(ai_response):
    """
    Extracts the estimated savings value from the AI response using regex.
    """
    match = re.search(r"\$?(\d+(?:,\d+)?(?:\.\d+)?)", ai_response)
    if match:
        return float(match.group(1).replace(",", ""))
    return 0.0  # Default if no valid number is found

def estimate_savings_with_ai(return_data):
    """
    Uses AI prompts to estimate cost savings for each product over 6 months.
    """
    total_savings = 0
    total_original_costs = 0
    results = []

    for item in return_data["returns"]:
        product_id = item["product_id"]
        name = item["name"]
        recyclability_percentage = item["recyclability_percentage"]
        yearly_sales = item["yearly_sales"]
        price_per_pound = item["price_per_pound"]
        weight = item["weight"]
        
        # Calculate original cost
        original_cost = yearly_sales * weight * price_per_pound
        total_original_costs += original_cost / 2  # 6 months cost
        
        print(f"\nCalculating savings for: {name}")
        print(f"Original Cost (6 Months): ${original_cost / 2:.2f}")
        time.sleep(1)
        
        # Construct AI prompt dynamically with structured savings categories
        prompt = f"""
        An e-commerce platform wants to estimate its savings over the next 6 months by optimizing recycling.
        The product "{name}" (ID: {product_id}) has a recyclability rate of {recyclability_percentage}%.
        It is sold {yearly_sales} times per year, each unit weighs {weight} lbs, and the material price per pound is ${price_per_pound}.
        
        Please analyze and provide structured savings estimates based on:
        1. **Resell Value** - If the product or materials can be resold at a discounted rate.
        2. **Recycling Revenue** - Expected income from recycling the materials.
        3. **Manufacturing Cost Reduction** - How much can be saved by reusing materials.
        4. **Waste Disposal Cost Avoidance** - Savings from not having to dispose of non-recyclable waste.
        5. **Best Recycling Methods** - Recommend the most effective recycling techniques for this product.
        
        Provide the total estimated savings in USD and a brief breakdown of these categories.
        """

        # Call AI Model
        ai_response = call_ai_model(prompt)

        # Extract numerical savings estimation from AI response using regex
        estimated_savings = extract_savings_from_ai_response(ai_response)

        total_savings += estimated_savings

        savings_percentage = (estimated_savings / (original_cost / 2)) * 100 if original_cost > 0 else 0
        
        print(f"Estimated Savings: ${estimated_savings:.2f}")
        print(f"Savings Percentage: {savings_percentage:.2f}%")
        time.sleep(1)

        results.append({
            "Product ID": product_id,
            "Name": name,
            "Recyclability (%)": recyclability_percentage,
            "Yearly Sales": yearly_sales,
            "Weight (lbs)": weight,
            "Price per Pound ($)": price_per_pound,
            "AI Estimated Savings (6 Months) ($)": round(estimated_savings, 2),
            "Savings Percentage (%)": round(savings_percentage, 2),
            "AI Response": ai_response
        })

    return total_savings, total_original_costs, results

# Load return data from JSON
if os.path.exists(RETURNS_JSON_PATH):
    with open(RETURNS_JSON_PATH, "r") as file:
        return_data = json.load(file)

    # Run AI estimation
    total_savings_6_months, total_original_costs_6_months, savings_results_6_months = estimate_savings_with_ai(return_data)

    # Save results to JSON
    with open(OUTPUT_JSON_PATH, "w") as output_file:
        json.dump({
            "total_savings": total_savings_6_months,
            "total_original_costs": total_original_costs_6_months,
            "savings_percentage": (total_savings_6_months / total_original_costs_6_months) * 100 if total_original_costs_6_months > 0 else 0,
            "detailed_results": savings_results_6_months
        }, output_file, indent=4)

    print(f"\nTotal Original Cost (6 Months): ${total_original_costs_6_months:.2f}")
    print(f"Total Estimated Savings for 6 Months (AI): ${total_savings_6_months:.2f}")
    print(f"Overall Savings Percentage: {(total_savings_6_months / total_original_costs_6_months) * 100:.2f}%")
    print(f"Results saved to {OUTPUT_JSON_PATH}")

else:
    print(f"Error: Returns file not found at {RETURNS_JSON_PATH}")