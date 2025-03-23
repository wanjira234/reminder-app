from database import engine, get_db
from models import User
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    # Get database session
    db = next(get_db())
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "epiphanywanjira@gmail.com").first()
        if existing_user:
            print("Test user already exists!")
            return
        
        # Create new user
        hashed_password = pwd_context.hash("your-password-here")  # Replace with your desired password
        test_user = User(
            email="epiphanywanjira@gmail.com",
            hashed_password=hashed_password
        )
        
        # Add and commit
        db.add(test_user)
        db.commit()
        print("Test user created successfully!")
        
    except Exception as e:
        print(f"Error creating test user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 