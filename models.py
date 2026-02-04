# from sqlalchemy.orm import Mapped, mapped_column
# from database import Base

# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str]
#     hashed_password: Mapped[str]

# class Todo(Base):
#     __tablename__ = "todos"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     task: Mapped[str]
#     completed: Mapped[bool] = mapped_column(default=False)
    