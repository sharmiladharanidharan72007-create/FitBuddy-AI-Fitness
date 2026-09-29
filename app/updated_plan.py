import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def fallback_update(
    original_plan,
    feedback
):

    return (
        original_plan
        + "\n\n"
        + "UPDATED USING USER FEEDBACK\n\n"
        + f"User requested:\n{feedback}\n\n"
        + "Fallback mode is active. "
        + "When Gemini API access is configured, "
        + "FitBuddy will regenerate the complete "
        + "7-day plan using this feedback."
    )


def update_workout_plan(
    username,
    age,
    weight,
    goal,
    intensity,
    original_plan,
    feedback
):

    prompt = f"""
You are FitBuddy,
an AI fitness planning assistant.

Update an existing 7-day workout plan
based on user feedback.


USER

Name: {username}

Age: {age}

Weight: {weight} kg

Goal: {goal}

Intensity: {intensity}


ORIGINAL PLAN

{original_plan}


USER FEEDBACK

{feedback}


REQUIREMENTS

Create a COMPLETE revised 7-day plan.

Do not only list the changes.

Apply the user's feedback.

Keep the fitness goal.

Keep the requested intensity.

Include:

- Day 1
- Day 2
- Day 3
- Day 4
- Day 5
- Day 6
- Day 7

Each day should include appropriate
workout/recovery information.

Include warm-up,
main workout,
sets/repetitions or duration,
rest,
and cooldown/recovery.

Use simple English.

Do not diagnose medical conditions.

Include a short safety note.
"""


    api_key = os.getenv(
        "GOOGLE_API_KEY",
        ""
    ).strip()


    if not api_key:

        return fallback_update(
            original_plan,
            feedback
        )


    try:

        client = genai.Client(
            api_key=api_key
        )


        model = os.getenv(
            "GEMINI_UPDATE_MODEL",
            "gemini-2.5-pro"
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

            return fallback_update(
                original_plan,
                feedback
            )

        raise


    return fallback_update(
        original_plan,
        feedback
    )