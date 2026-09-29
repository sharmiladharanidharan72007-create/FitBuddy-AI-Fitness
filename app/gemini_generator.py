import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def get_gemini_client():

    api_key = os.getenv(
        "GOOGLE_API_KEY",
        ""
    ).strip()

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def fallback_workout_plan(
    username,
    age,
    weight,
    goal,
    intensity
):

    return f"""
FITBUDDY 7-DAY WORKOUT PLAN

User: {username}

Age: {age}
Weight: {weight} kg
Goal: {goal.title()}
Intensity: {intensity.title()}


DAY 1 - FULL BODY

Warm-up:
5-10 minutes of easy walking and mobility.

Main Workout:
- Bodyweight Squats: 3 x 10
- Wall/Incline Push-ups: 3 x 8
- Glute Bridges: 3 x 12
- Plank: 3 x 20 seconds

Rest:
45-60 seconds between sets.

Cooldown:
5 minutes of gentle stretching.


DAY 2 - CARDIO

Warm-up:
5 minutes easy walking.

Main Workout:
25-30 minutes comfortable cardio.

Cooldown:
5 minutes slow walking and stretching.


DAY 3 - LOWER BODY

Warm-up:
5-10 minutes mobility.

Main Workout:
- Squats: 3 x 10
- Reverse Lunges: 3 x 8 each side
- Calf Raises: 3 x 12
- Glute Bridges: 3 x 12

Cooldown:
5 minutes.


DAY 4 - RECOVERY

Activity:
15-20 minutes easy walking.

Add:
Gentle full-body mobility.

Keep the intensity low.


DAY 5 - UPPER BODY AND CORE

Warm-up:
5-10 minutes.

Main Workout:
- Incline Push-ups: 3 x 8
- Backpack/Resistance Rows: 3 x 10
- Shoulder Raises: 2 x 10
- Dead Bug: 3 x 8 each side

Cooldown:
5 minutes.


DAY 6 - CARDIO

Warm-up:
5 minutes.

Main Workout:
20-30 minutes cardio at a sustainable pace.

Cooldown:
5 minutes.


DAY 7 - ACTIVE RECOVERY

Activity:
20-30 minutes easy walking.

Add:
Gentle stretching and mobility.

Focus on recovery.


PROGRESSION:

Start comfortably.

Gradually increase repetitions,
duration, or resistance.

Do not force high intensity.


SAFETY:

Stop exercise if you experience
sharp pain, dizziness, chest pain,
or unusual shortness of breath.

Seek appropriate professional
guidance when necessary.
""".strip()


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    prompt = f"""
You are FitBuddy,
an AI fitness planning assistant.

Create a personalized 7-day workout plan.

USER INFORMATION

Name: {username}

Age: {age}

Weight: {weight} kg

Fitness Goal: {goal}

Preferred Intensity: {intensity}


REQUIREMENTS

1. Create exactly 7 days.

2. Give every day a workout focus.

3. Include warm-up.

4. Include the main workout.

5. Include sets and repetitions
   or duration.

6. Include rest guidance.

7. Include cooldown or recovery.

8. Match the selected intensity.

9. Keep the language simple.

10. Do not diagnose medical conditions.

11. Include a short safety note.

Format the answer using clear
DAY 1, DAY 2, etc. headings.
"""


    client = get_gemini_client()


    # No API key
    if client is None:

        return fallback_workout_plan(
            username,
            age,
            weight,
            goal,
            intensity
        )


    model = os.getenv(
        "GEMINI_WORKOUT_MODEL",
        "gemini-2.5-pro"
    )


    try:

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

            return fallback_workout_plan(
                username,
                age,
                weight,
                goal,
                intensity
            )

        raise


    return fallback_workout_plan(
        username,
        age,
        weight,
        goal,
        intensity
    )