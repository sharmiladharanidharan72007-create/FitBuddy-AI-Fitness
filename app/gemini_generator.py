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

User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}
Health Information: {health_problem}

========================
DAY 1
========================

WORKOUT
• Warm-up: 5-10 minutes walking
• Main workout: Bodyweight squats, wall push-ups, lunges
• Sets: 3 sets
• Repetitions: 10-12 each
• Rest: 60 seconds
• Cool-down: 5 minutes stretching

FOOD
• Breakfast: Idli with sambar and fruit
• Lunch: Rice with dal and vegetables
• Evening Snack: Banana and a small handful of nuts
• Dinner: Chapati with vegetable curry


========================
DAY 2
========================

WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Brisk walking and light strength exercises
• Duration: 25-30 minutes
• Rest: As needed
• Cool-down: 5 minutes stretching

FOOD
• Breakfast: Dosa with sambar
• Lunch: Rice with vegetables and curd
• Evening Snack: Apple or other seasonal fruit
• Dinner: Chapati with dal and vegetables


========================
DAY 3
========================

WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Glute bridges, wall push-ups and step-ups
• Sets: 3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 5 minutes stretching

FOOD
• Breakfast: Oats with banana
• Lunch: Rice with dal and vegetables
• Evening Snack: Yogurt and fruit
• Dinner: Vegetable dosa with sambar


========================
DAY 4
========================

WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Light cardio and stretching
• Duration: 25-30 minutes
• Rest: As needed
• Cool-down: 5-10 minutes

FOOD
• Breakfast: Pongal with sambar
• Lunch: Rice with vegetables and curd
• Evening Snack: Fruit and nuts
• Dinner: Chapati with vegetable curry


========================
DAY 5
========================

WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Squats, lunges and modified push-ups
• Sets: 3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 5 minutes

FOOD
• Breakfast: Idli with sambar
• Lunch: Rice with dal and vegetables
• Evening Snack: Banana or seasonal fruit
• Dinner: Chapati with dal


========================
DAY 6
========================

WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Brisk walking and full-body stretching
• Duration: 30 minutes
• Rest: As needed
• Cool-down: 5-10 minutes

FOOD
• Breakfast: Vegetable upma with fruit
• Lunch: Rice with vegetables and curd
• Evening Snack: Nuts and fruit
• Dinner: Dosa with vegetable sambar


========================
DAY 7
========================

WORKOUT
• Warm-up: 5-10 minutes
• Main workout: Light full-body workout
• Sets: 2-3
• Repetitions: 10-12
• Rest: 60 seconds
• Cool-down: 10 minutes stretching

FOOD
• Breakfast: Dosa with sambar and fruit
• Lunch: Rice with dal and vegetables
• Evening Snack: Fruit or yogurt
• Dinner: Chapati with vegetable curry


IMPORTANT
This is general wellness guidance.
It is not medical diagnosis or treatment.
"""


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity,
    health_problem
):

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

Create a personalized 7-day workout and food plan.

USER DETAILS
Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}
Health Information: {health_problem}

Create exactly 7 days.

For EVERY DAY provide:

WORKOUT
1. Warm-up
2. Main exercises
3. Sets and repetitions OR duration
4. Rest
5. Cool-down

FOOD
1. Breakfast
2. Lunch
3. Evening snack
4. Dinner

FOOD PLAN REQUIREMENTS
- Give practical and simple food choices.
- Use common foods where possible.
- Provide variety across the 7 days.
- Do not ask the user what food they normally eat.
- Generate the food suggestions yourself.
- Consider the user's fitness goal.
- Do not claim that the food plan treats or cures a disease.

SAFETY
If a health problem is reported, avoid exercises that could obviously aggravate
that problem and include a brief suggestion to consult a qualified healthcare
professional when appropriate.

Do not diagnose any medical condition.

Use this exact structure:

DAY 1
WORKOUT
Warm-up:
Main workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:

FOOD
Breakfast:
Lunch:
Evening Snack:
Dinner:

DAY 2
WORKOUT
Warm-up:
Main workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:

FOOD
Breakfast:
Lunch:
Evening Snack:
Dinner:

Continue the same structure through DAY 7.

At the end, add a short general hydration/recovery tip.

This is general wellness guidance and not medical advice.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )

        if response and response.text:
            return response.text

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