from sqlmodel import Session, SQLModel, create_engine

DATABSE_URL = "sqlite:///dabbewala.db"

engine = create_engine(DATABSE_URL, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """Gets a new DB session"""
    with Session(engine) as session:
        yield session
