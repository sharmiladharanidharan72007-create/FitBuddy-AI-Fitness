from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session


from .database import (
    get_db,
    get_all_users,
    get_latest_plan,
    get_user,
    save_plan,
    save_user,
    update_plan
)

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .gemini_generator import (
    generate_workout_gemini
)

from .models import User

from .schemas import (
    FeedbackRequest,
    UserInput
)

from .updated_plan import (
    update_workout_plan
)


BASE_DIR = Path(
    __file__
).resolve().parent.parent


templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)


router = APIRouter()


def render_error(
    request,
    message
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": message
        },
        status_code=400
    )


# =========================================================
# HOME PAGE
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# =========================================================
# GENERATE WORKOUT
# =========================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)
):


    # Validate input

    try:

        data = UserInput(

            username=username,

            user_id=user_id,

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity
        )


    except Exception as error:

        return render_error(
            request,
            f"Please check your input: {error}"
        )


    # Check if user already exists

    user = get_user(
        db,
        data.user_id
    )


    if user:

        user.username = data.username

        user.age = data.age

        user.weight = data.weight

        user.goal = data.goal

        user.intensity = data.intensity

        db.commit()

        db.refresh(user)


    else:

        user = User(

            username=data.username,

            user_id=data.user_id,

            age=data.age,

            weight=data.weight,

            goal=data.goal,

            intensity=data.intensity

        )

        save_user(
            db,
            user
        )


    # Generate workout

    try:

        workout_plan = generate_workout_gemini(

            data.username,

            data.age,

            data.weight,

            data.goal,

            data.intensity

        )


        nutrition_tip = (
            generate_nutrition_tip_with_flash(
                data.goal
            )
        )


    except Exception as error:

        return render_error(
            request,
            f"AI generation failed: {error}"
        )


    # Save plan

    plan = save_plan(

        db,

        data.user_id,

        workout_plan,

        nutrition_tip

    )


    # Show result page

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "user": user,

            "plan": plan,

            "workout_plan":
                plan.current_plan,

            "nutrition_tip":
                plan.nutrition_tip,

            "message": None

        }

    )


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)

):


    # Validate feedback

    try:

        data = FeedbackRequest(

            user_id=user_id,

            feedback=feedback

        )


    except Exception as error:

        return render_error(

            request,

            f"Please check your feedback: {error}"

        )


    # Get user

    user = get_user(

        db,

        data.user_id

    )


    # Get plan

    plan = get_latest_plan(

        db,

        data.user_id

    )


    if not user or not plan:

        return render_error(

            request,

            "User or workout plan was not found."

        )


    # Update plan

    try:

        revised_plan = update_workout_plan(

            user.username,

            user.age,

            user.weight,

            user.goal,

            user.intensity,

            plan.current_plan,

            data.feedback

        )


        updated_plan = update_plan(

            db,

            plan,

            revised_plan,

            data.feedback

        )


    except Exception as error:

        return render_error(

            request,

            f"Plan update failed: {error}"

        )


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "user": user,

            "plan": updated_plan,

            "workout_plan":
                updated_plan.current_plan,

            "nutrition_tip":
                updated_plan.nutrition_tip,

            "message":
                "Your plan has been updated using your feedback."

        }

    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db)

):

    users = get_all_users(db)


    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={

            "users": users

        }

    )


# =========================================================
# API - ALL USERS
# =========================================================

@router.get(
    "/api/users"
)
def api_users(

    db: Session = Depends(get_db)

):

    users = get_all_users(db)


    return [

        {

            "id": user.id,

            "user_id": user.user_id,

            "username": user.username,

            "age": user.age,

            "weight": user.weight,

            "goal": user.goal,

            "intensity": user.intensity,

            "created_at":
                user.created_at.isoformat()
                if user.created_at
                else None

        }

        for user in users

    ]


# =========================================================
# API - ONE USER
# =========================================================

@router.get(
    "/api/users/{user_id}"
)
def api_user(

    user_id: str,

    db: Session = Depends(get_db)

):

    user = get_user(

        db,

        user_id

    )


    plan = get_latest_plan(

        db,

        user_id

    )


    if not user:

        return JSONResponse(

            {
                "detail":
                    "User not found"
            },

            status_code=404

        )


    return {

        "user": {

            "id": user.id,

            "user_id": user.user_id,

            "username": user.username,

            "age": user.age,

            "weight": user.weight,

            "goal": user.goal,

            "intensity": user.intensity

        },


        "plan":

            None

            if not plan

            else {

                "original_plan":
                    plan.original_plan,

                "current_plan":
                    plan.current_plan,

                "nutrition_tip":
                    plan.nutrition_tip,

                "feedback":
                    plan.feedback

            }

    }