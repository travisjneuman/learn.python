# ============================================================================
# Project 04 — Authentication
# ============================================================================
# This project adds user accounts to the todo API. Users register, log in
# to receive a JWT token, and use that token to access protected endpoints.
# Each user can only see and manage their own todos.
#
# New concepts:
# 1. Password hashing with bcrypt (never store plaintext passwords)
# 2. JWT tokens for stateless authentication
# 3. Protected endpoints using Depends(get_current_user)
# 4. Foreign key relationships (todos belong to users)
#
# Run: python app.py
# Docs: http://127.0.0.1:8000/docs
# ============================================================================

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import engine, Base
from models import User, Todo
from schemas import UserCreate, UserResponse, Token, TodoCreate, TodoUpdate, TodoResponse
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_db,
)

# Create all database tables on startup.
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ============================================================================
# User endpoints (public — no authentication required)
# ============================================================================


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user.

    Steps:
    1. Check if the username already exists.
    2. Hash the password (never store plaintext).
    3. Create the user in the database.
    4. Return user info (without the password hash).
    """
    # Check for duplicate username.
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Create the user with a hashed password.
    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    """Log in and receive a JWT token.

    Steps:
    1. Find the user by username.
    2. Verify the password against the stored hash.
    3. Create and return a JWT token.

    The token contains the username as the "sub" (subject) claim. The client
    sends this token in the Authorization header for all subsequent requests.
    """
    # Look up the user.
    db_user = db.query(User).filter(User.username == user.username).first()

    # If the user does not exist or the password is wrong, return 401.
    # We use the same error message for both cases so attackers cannot
    # determine whether a username exists.
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Create a JWT token with the username as the subject.
    access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer"}


# ============================================================================
# Todo endpoints (protected — require authentication)
# ============================================================================
# Every endpoint below includes `current_user: User = Depends(get_current_user)`.
# This means FastAPI will:
# 1. Extract the Bearer token from the Authorization header.
# 2. Verify and decode the JWT.
# 3. Look up the user in the database.
# 4. Pass the User object as current_user.
#
# If the token is missing, invalid, or expired, FastAPI returns 401 before
# your endpoint code runs. You never see unauthenticated requests.
# ============================================================================


@app.get("/todos", response_model=list[TodoResponse])
def list_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all todos belonging to the current user.

    The filter ensures users only see their own todos, not everyone's.
    """
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a single todo by ID, only if it belongs to the current user."""
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new todo owned by the current user.

    The user_id is set from the JWT token, not from the request body.
    This prevents users from creating todos under someone else's account.
    """
    db_todo = Todo(
        title=todo.title,
        user_id=current_user.id,  # Set owner from the authenticated user
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a todo, only if it belongs to the current user."""
    db_todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a todo, only if it belongs to the current user."""
    db_todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()


# ============================================================================
# Run the server
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
