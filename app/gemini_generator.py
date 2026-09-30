import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def fallback_workout_plan(
    username,
    age,
    weight,
    goal,
    intensity,
    health_problem
):
    return f"""
FITBUDDY 7-DAY PERSONALIZED PLAN

👤 USER PROFILE
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Workout Intensity: {intensity}

❤️ HEALTH INFORMATION
Reported Health Problem:
{health_problem}

━━━━━━━━━━━━━━━━━━━━
DAY 1
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Light full-body exercises
• Sets: 2-3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 5 minutes

🥗 FOOD
• Breakfast: Idli with sambar and fruit
• Lunch: Rice with dal and vegetables
• Evening Snack: Banana and nuts
• Dinner: Chapati with vegetable curry


━━━━━━━━━━━━━━━━━━━━
DAY 2
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Light walking and gentle exercises
• Duration: 20-30 minutes
• Rest: As needed
• Cool-down: 5 minutes

🥗 FOOD
• Breakfast: Dosa with sambar
• Lunch: Rice with vegetables and curd
• Evening Snack: Apple or seasonal fruit
• Dinner: Chapati with dal


━━━━━━━━━━━━━━━━━━━━
DAY 3
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Wall push-ups, gentle bridges and stretching
• Sets: 2-3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 5 minutes

🥗 FOOD
• Breakfast: Oats with banana
• Lunch: Rice with dal and vegetables
• Evening Snack: Yogurt and fruit
• Dinner: Vegetable dosa with sambar


━━━━━━━━━━━━━━━━━━━━
DAY 4
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Light cardio and stretching
• Duration: 20-30 minutes
• Rest: As needed
• Cool-down: 5-10 minutes

🥗 FOOD
• Breakfast: Pongal with sambar
• Lunch: Rice with vegetables and curd
• Evening Snack: Fruit and nuts
• Dinner: Chapati with vegetable curry


━━━━━━━━━━━━━━━━━━━━
DAY 5
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Gentle strength exercises
• Sets: 2-3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 5 minutes

🥗 FOOD
• Breakfast: Idli with sambar
• Lunch: Rice with dal and vegetables
• Evening Snack: Banana or seasonal fruit
• Dinner: Chapati with dal


━━━━━━━━━━━━━━━━━━━━
DAY 6
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Walking and full-body stretching
• Duration: 25-30 minutes
• Rest: As needed
• Cool-down: 5-10 minutes

🥗 FOOD
• Breakfast: Vegetable upma with fruit
• Lunch: Rice with vegetables and curd
• Evening Snack: Nuts and fruit
• Dinner: Dosa with vegetable sambar


━━━━━━━━━━━━━━━━━━━━
DAY 7
━━━━━━━━━━━━━━━━━━━━

🏋️ WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Gentle full-body workout
• Sets: 2-3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 10 minutes stretching

🥗 FOOD
• Breakfast: Dosa with sambar and fruit
• Lunch: Rice with dal and vegetables
• Evening Snack: Fruit or yogurt
• Dinner: Chapati with vegetable curry


━━━━━━━━━━━━━━━━━━━━

❤️ HEALTH CONSIDERATION

Reported problem:
{health_problem}

The workout should be adjusted according to the reported
health information. This is general wellness guidance and
does not diagnose or treat medical conditions.

If the reported problem may make exercise unsafe, consult
a qualified healthcare professional before exercising.
"""


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity,
    health_problem
):

    if not health_problem or not health_problem.strip():
        health_problem = "No problem reported"

    if not client:
        return fallback_workout_plan(
            username,
            age,
            weight,
            goal,
            intensity,
            health_problem
        )

    prompt = f"""
You are FitBuddy, an AI fitness and wellness planning assistant.

Create a personalized 7-day fitness and food plan.

━━━━━━━━━━━━━━━━━━━━
USER INFORMATION
━━━━━━━━━━━━━━━━━━━━

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

REPORTED HEALTH INFORMATION:
{health_problem}

━━━━━━━━━━━━━━━━━━━━
HEALTH-AWARE PLANNING
━━━━━━━━━━━━━━━━━━━━

The user can enter ANY health problem, symptom, injury,
physical limitation, or other health-related information.

Do not assume that the reported problem is one of a fixed list.

Read the exact health information provided by the user and
consider it when creating the workout.

If a health problem is reported:

• Adjust the workout appropriately.
• Avoid exercises that could obviously aggravate the reported problem.
• Suggest safer alternatives where appropriate.
• Adjust intensity, duration, or rest when appropriate.
• Clearly explain the important workout modification.
• If the condition may make exercise unsafe, recommend consulting
  a qualified healthcare professional before exercising.
• Do not diagnose the user's condition.
• Do not claim to treat or cure the condition.

If the user says "No problem reported", create the normal workout
based on the user's goal and selected intensity.

━━━━━━━━━━━━━━━━━━━━
7-DAY WORKOUT
━━━━━━━━━━━━━━━━━━━━

Create exactly 7 days.

For every day include:

🏋️ Warm-up
🔥 Main workout
🔢 Sets/Repetitions or Duration
⏱️ Rest
🧘 Cool-down

━━━━━━━━━━━━━━━━━━━━
7-DAY FOOD PLAN
━━━━━━━━━━━━━━━━━━━━

Generate the food plan automatically.

Do NOT ask the user what they normally eat.

For every day include:

🍳 Breakfast
🍚 Lunch
🍎 Evening Snack
🥗 Dinner

Use practical and common foods.

Provide variety across the 7 days.

Consider the user's fitness goal.

Do not claim that food treats or cures a disease.

━━━━━━━━━━━━━━━━━━━━
REQUIRED FORMAT
━━━━━━━━━━━━━━━━━━━━

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


DAY 2

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

━━━━━━━━━━━━━━━━━━━━
HEALTH CONSIDERATION
━━━━━━━━━━━━━━━━━━━━

Reported problem:
{health_problem}

Explain briefly how the workout was adjusted based on the
reported health information.

━━━━━━━━━━━━━━━━━━━━
RECOVERY TIP
━━━━━━━━━━━━━━━━━━━━

Give one short general hydration or recovery tip.

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

        print("Gemini generation error:", e)

    return fallback_workout_plan(
        username,
        age,
        weight,
        goal,
        intensity,
        health_problem
    )