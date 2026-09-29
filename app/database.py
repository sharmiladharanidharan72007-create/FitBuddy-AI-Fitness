from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def init_db():

    # Import models before creating tables
    from . import models

    Base.metadata.create_all(bind=engine)


def save_user(db, user):

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def get_user(db, user_id):

    from .models import User

    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def get_all_users(db):

    from .models import User

    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )


def save_plan(
    db,
    user_id,
    workout_plan,
    nutrition_tip
):

    from .models import FitnessPlan

    plan = FitnessPlan(
        user_id=user_id,
        original_plan=workout_plan,
        current_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)

    db.commit()

    db.refresh(plan)

    return plan


def get_latest_plan(db, user_id):

    from .models import FitnessPlan

    return (
        db.query(FitnessPlan)
        .filter(FitnessPlan.user_id == user_id)
        .order_by(FitnessPlan.created_at.desc())
        .first()
    )


def update_plan(
    db,
    plan,
    updated_plan,
    feedback
):

    plan.current_plan = updated_plan

    plan.feedback = feedback

    db.commit()

    db.refresh(plan)

    return plan