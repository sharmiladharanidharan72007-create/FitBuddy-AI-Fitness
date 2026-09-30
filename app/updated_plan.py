import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def update_workout_plan(
    username,
    age,
    weight,
    goal,
    intensity,
    health_problem,
    original_plan,
    feedback
):
    """
    Update the existing FitBuddy plan based on user feedback.
    """

    # If Gemini API is not available, keep the original plan
    # and add a clear feedback note.
    if not client:

        return f"""
{original_plan}

━━━━━━━━━━━━━━━━━━━━
✅ FEEDBACK RECEIVED
━━━━━━━━━━━━━━━━━━━━

Your feedback:
{feedback}

The feedback has been received.
Please regenerate the plan when the Gemini API is available.
"""

    prompt = f"""
You are FitBuddy, an AI fitness and wellness planning assistant.

The user already has a 7-day fitness and food plan.

The user has now provided feedback.

Your task is to MODIFY the existing plan according to the
user's feedback and create a new improved 7-day plan.

━━━━━━━━━━━━━━━━━━━━
USER INFORMATION
━━━━━━━━━━━━━━━━━━━━

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Reported Health Problem:
{health_problem}

━━━━━━━━━━━━━━━━━━━━
USER FEEDBACK
━━━━━━━━━━━━━━━━━━━━

{feedback}

━━━━━━━━━━━━━━━━━━━━
EXISTING PLAN
━━━━━━━━━━━━━━━━━━━━

{original_plan}

━━━━━━━━━━━━━━━━━━━━
UPDATE RULES
━━━━━━━━━━━━━━━━━━━━

1. Read the user's feedback carefully.

2. Modify the existing plan according to the feedback.

3. Do not simply repeat the old plan.

4. Keep the user's fitness goal in mind.

5. Keep the user's reported health information in mind.

6. If the user says the workout is too difficult:
   - reduce intensity,
   - reduce repetitions or duration,
   - provide easier alternatives.

7. If the user says the workout is too easy:
   - increase difficulty gradually when appropriate.

8. If the user asks to change an exercise:
   - replace it with a suitable alternative.

9. If the user asks for more rest:
   - increase rest periods or reduce workout volume.

10. If the user asks for different food:
    - provide practical alternative food choices.

11. Keep the plan as a 7-day plan.

12. Keep both workout and food sections.

13. Consider any health problem reported by the user.

14. Do not diagnose, treat, or claim to cure a medical condition.

15. If the health information could make exercise unsafe,
    recommend consulting a qualified healthcare professional.

━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━

Start with:

🔄 UPDATED FITBUDDY PLAN

Then provide:

DAY 1

🏋️ WORKOUT
Warm-up:
Main workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:

🥗 FOOD
Breakfast:
Lunch:
Evening Snack:
Dinner:

Continue the same format through DAY 7.

At the end include:

💡 CHANGES MADE FROM FEEDBACK

Briefly explain what was changed based on the user's feedback.

❤️ HEALTH CONSIDERATION

Briefly mention how the reported health information was considered.

💧 RECOVERY TIP

Give one short general recovery or hydration tip.

This is general wellness guidance and is not medical advice.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

    except Exception as e:

        print("Feedback update error:", e)

    # If Gemini fails, return the original plan
    # instead of crashing the application.
    return f"""
{original_plan}

━━━━━━━━━━━━━━━━━━━━
⚠️ FEEDBACK RECEIVED
━━━━━━━━━━━━━━━━━━━━

Your feedback:
{feedback}

The plan could not be regenerated at this moment.
Please try again.
"""