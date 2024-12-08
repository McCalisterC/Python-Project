from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(Integer)
    xp: Mapped[int] = mapped_column(Integer)
    characters: Mapped[list["Character"]] = relationship("Character", back_populates="account")

class Character(Base):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(Integer)
    xp: Mapped[int] = mapped_column(Integer)
    defeated_enemies: Mapped[int] = mapped_column(Integer)
    secrets: Mapped[int] = mapped_column(Integer)
    vitality: Mapped[int] = mapped_column(Integer)
    strength: Mapped[int] = mapped_column(Integer)
    dexterity: Mapped[int] = mapped_column(Integer)
    defense: Mapped[int] = mapped_column(Integer)
    sprite_path: Mapped[int] = mapped_column(Integer)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship("Account", back_populates="characters")

# Set up the database URL
DATABASE_URL = "sqlite:///gamedatabase.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

#Password pattern
regex = r"^[!@#$%^&].*(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,12}$"