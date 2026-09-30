from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import (
    get_db,
    get_user,
    get_all_users,
    save_user,
    save_plan,
    get_latest_plan,
    update_plan,
)

from .models import User
from .schemas import UserInput, FeedbackRequest

from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# =========================================================
# HOME PAGE
# =========================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "updated": False
        }
    )


# =========================================================
# GENERATE NEW FITNESS PLAN
# =========================================================

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    health_problem: str = Form(""),

    db: Session = Depends(get_db)
):

    try:

        user_input = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            health_problem=health_problem
        )

    except Exception as e:

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e),
                "updated": False
            }
        )

    # -----------------------------------------------------
    # Check whether user already exists
    # -----------------------------------------------------

    user = get_user(
        db,
        user_input.user_id
    )

    if user:

        user.username = user_input.username
        user.age = user_input.age
        user.weight = user_input.weight
        user.goal = user_input.goal
        user.intensity = user_input.intensity
        user.health_problem = user_input.health_problem

        db.commit()
        db.refresh(user)

    else:

        user = User(
            username=user_input.username,
            user_id=user_input.user_id,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
            health_problem=user_input.health_problem
        )

        save_user(
            db,
            user
        )

    # -----------------------------------------------------
    # Generate AI workout + food plan
    # -----------------------------------------------------

    workout_plan = generate_workout_gemini(
        user_input.username,
        user_input.age,
        user_input.weight,
        user_input.goal,
        user_input.intensity,
        user_input.health_problem
    )

    # -----------------------------------------------------
    # Generate nutrition/recovery tip
    # -----------------------------------------------------

    nutrition_tip = generate_nutrition_tip_with_flash(
        user_input.goal
    )

    # -----------------------------------------------------
    # Save plan
    # -----------------------------------------------------

    save_plan(
        db,
        user_input.user_id,
        workout_plan,
        nutrition_tip
    )

    # -----------------------------------------------------
    # Show result page
    # -----------------------------------------------------

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,

            "username": user_input.username,

            "user_id": user_input.user_id,

            "age": user_input.age,

            "weight": user_input.weight,

            "goal": user_input.goal,

            "intensity": user_input.intensity,

            "health_problem": user_input.health_problem,

            "workout_plan": workout_plan,

            "nutrition_tip": nutrition_tip,

            "updated": False,

            "success_message": ""
        }
    )


# =========================================================
# SUBMIT FEEDBACK AND UPDATE PLAN
# =========================================================

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)

):

    # -----------------------------------------------------
    # Find user
    # -----------------------------------------------------

    user = get_user(
        db,
        user_id
    )

    if not user:

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,

                "error": "User not found.",

                "updated": False
            }
        )

    # -----------------------------------------------------
    # Find latest plan
    # -----------------------------------------------------

    plan = get_latest_plan(
        db,
        user_id
    )

    if not plan:

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,

                "error": "No fitness plan found.",

                "updated": False
            }
        )

    # -----------------------------------------------------
    # Validate feedback
    # -----------------------------------------------------

    try:

        feedback_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback
        )

    except Exception as e:

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,

                "username": user.username,

                "user_id": user.user_id,

                "age": user.age,

                "weight": user.weight,

                "goal": user.goal,

                "intensity": user.intensity,

                "health_problem": user.health_problem,

                "workout_plan": plan.current_plan,

                "nutrition_tip": plan.nutrition_tip,

                "updated": False,

                "success_message": "",

                "error": str(e)
            }
        )

    # -----------------------------------------------------
    # Ask Gemini to update the plan
    # -----------------------------------------------------

    updated_plan = update_workout_plan(

        user.username,

        user.age,

        user.weight,

        user.goal,

        user.intensity,

        user.health_problem,

        plan.current_plan,

        feedback_data.feedback
    )

    # -----------------------------------------------------
    # Save updated plan to database
    # -----------------------------------------------------

    update_plan(

        db,

        plan,

        updated_plan,

        feedback_data.feedback
    )

    # -----------------------------------------------------
    # Show updated result page
    # -----------------------------------------------------

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,

            "username": user.username,

            "user_id": user.user_id,

            "age": user.age,

            "weight": user.weight,

            "goal": user.goal,

            "intensity": user.intensity,

            "health_problem": user.health_problem,

            "workout_plan": updated_plan,

            "nutrition_tip": plan.nutrition_tip,

            "updated": True,

            "success_message":
                "Your feedback has been received and your fitness plan has been updated successfully!",

            "feedback_text": feedback_data.feedback
        }
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db)

):

    users = get_all_users(db)

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,

            "users": users
        }
    )


# =========================================================
# API - VIEW ALL USERS
# =========================================================

@router.get("/api/users")
def api_users(

    db: Session = Depends(get_db)

):

    users = get_all_users(db)

    return [

        {
            "user_id": user.user_id,

            "username": user.username,

            "age": user.age,

            "weight": user.weight,

            "goal": user.goal,

            "intensity": user.intensity,

            "health_problem": user.health_problem,

            "created_at": user.created_at
        }

        for user in users

    ]