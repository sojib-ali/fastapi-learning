from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    email: Mapped[str] = mapped_column(String(1024), index = True, unique=True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable = False)

class AccessToken(Base):
    __tableName__ = "access_token"