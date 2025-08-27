from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
import pytest
from models import Todos


# Use in-memory database for better isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    # Fixed: Use 'user_id' instead of 'id' to match your API filter
    return {'username': 'PixelPanda', 'user_id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="need to learn every day",
        priority=5,
        complete=False,
        owner_id=1,  # This matches the user_id in our mock user
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    yield todo
    
    # Cleanup
    db.query(Todos).delete()
    db.commit()
    db.close()