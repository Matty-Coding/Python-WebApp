from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime, timezone, timedelta

db = SQLAlchemy()


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hash_pwd: Mapped[str] = mapped_column(String(255), nullable=False)
    authenticated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    email_tokens = relationship(
        "EmailToken", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "authenticated": self.authenticated,
            "created_at": self.created_at,
        }


class EmailToken(db.Model):

    __tablename__ = "email_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=1)
    )

    user = relationship("User", back_populates="email_tokens")

    def __repr__(self):
        return f"<EmailToken {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "is_used": self.is_used,
            "expires_at": self.expires_at,
        }
