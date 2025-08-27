from passlib.context import CryptContext  # type: ignore
from database import SessionLocal, engine
from models import Users, Base

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Create the tables if they don't already exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# create a test user
user = Users(
    email="alice@example.com",
    username="alice",
    first_name="Alice",
    last_name="Tester",
    hashed_password=pwd_ctx.hash("secret"),  # password will be 'secret'
    is_active=True,
    role="user"
)

# create an admin user
admin_user = Users(
    email="dwiti@example.com",
    username="Fastapi_user",
    first_name="Dwiti",
    last_name="Thaker",
    hashed_password=pwd_ctx.hash("hello"),  # password will be 'hello'
    is_active=True,
    role="admin"
)

# add both users
db.add(user)
db.add(admin_user)

db.commit()
db.close()

print("✅ Users created: alice / secret AND Fastapi_user / hello")
