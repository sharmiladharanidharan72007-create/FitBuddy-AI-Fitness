import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def generate_nutrition_tip_with_flash(goal):

    fallback_tip = (
        "Drink enough water throughout the day and include vegetables, "
        "fruits, whole grains, and protein-rich foods in your meals. "
        "Choose food portions according to your personal needs and activity level."
    )

    if not client:
        return fallback_tip

    prompt = f"""
Give one short general nutrition and recovery tip for a person
whose fitness goal is: {goal}.

Keep it to 2-4 simple sentences.

Do not diagnose or treat any medical condition.
Do not create a 7-day food plan because the main Gemini model
already creates the 7-day food plan.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

    except Exception as e:

        print("Gemini Flash error:", e)

    return fallback_tip