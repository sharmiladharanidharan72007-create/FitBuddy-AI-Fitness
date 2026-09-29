import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def fallback_tip(goal):

    tips = {

        "weight loss":
        "Build meals around vegetables, a protein source, whole-food carbohydrates, and water. Focus on sustainable habits instead of extreme restriction.",

        "muscle gain":
        "Include a protein source in regular meals and snacks, along with enough overall food and fluids to support training and recovery.",

        "general wellness":
        "Choose varied foods, drink enough water, and maintain regular meals that support your daily activity and recovery.",

        "flexibility":
        "Stay hydrated and include balanced meals with protein and fruits or vegetables. Adequate sleep and recovery also support consistent training."

    }

    return tips.get(
        goal,
        tips["general wellness"]
    )


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
Give one concise and practical
nutrition or recovery tip.

Fitness goal:
{goal}

Requirements:

- 2 to 4 sentences.
- Simple English.
- Practical.
- General wellness advice.
- Do not provide medical treatment.
"""


    api_key = os.getenv(
        "GOOGLE_API_KEY",
        ""
    ).strip()


    if not api_key:

        return fallback_tip(goal)


    try:

        client = genai.Client(
            api_key=api_key
        )


        model = os.getenv(
            "GEMINI_TIP_MODEL",
            "gemini-2.5-flash"
        )


        response = client.models.generate_content(
            model=model,
            contents=prompt
        )


        generated_text = getattr(
            response,
            "text",
            None
        )


        if generated_text:

            return generated_text.strip()


    except Exception:

        if os.getenv(
            "ALLOW_FALLBACK",
            "true"
        ).lower() == "true":

            return fallback_tip(goal)

        raise


    return fallback_tip(goal)