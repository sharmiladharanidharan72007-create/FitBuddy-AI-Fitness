
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .database import Base


class User(Base):

    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True,
        nullable=False
    )


    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )


    goal: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    intensity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

intensity: Mapped[str] = mapped_column(
    String(20),
    nullable=False
)


health_problem: Mapped[str] = mapped_column(
    String(300),
    default="No problem reported",
    nullable=False
)
    




    


    health_problem: Mapped[str] = mapped_column(
        String(300),
        default="No problem reported",
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    plans: Mapped[list["FitnessPlan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )



class FitnessPlan(Base):

    __tablename__ = "fitness_plans"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id: Mapped[str] = mapped_column(
        String(80),
        ForeignKey("users.user_id"),
        index=True,
        nullable=False
    )


    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    current_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    nutrition_tip: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    user: Mapped[User] = relationship(
        back_populates="plans"
    )

