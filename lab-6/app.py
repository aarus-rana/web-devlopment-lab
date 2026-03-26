from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import bcrypt
from db import database, engine, metadata
from models import users, todos
from schema import UserCreate, UserLogin, TodoCreate, TodoUpdate, TodoResponse
from typing import List

# Create tables if they don't exist
metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    # Check if user already exists
    query = users.select().where(users.c.username == user.username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash password and store in db
    hashed_password = get_password_hash(user.password)
    query = users.insert().values(username=user.username, password=hashed_password)
    last_record_id = await database.execute(query)
    
    return {"message": "User registered successfully", "user_id": last_record_id}

@app.post("/login")
async def login(user: UserLogin):
    # Retrieve user from db
    query = users.select().where(users.c.username == user.username)
    db_user = await database.fetch_one(query)
    
    # Check username
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
    # Verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
    return {"message": "Login successful", "user_id": db_user["id"], "username": db_user["username"]}

@app.get("/todos/{user_id}", response_model=List[TodoResponse])
async def get_todos(user_id: int):
    query = todos.select().where(todos.c.user_id == user_id)
    return await database.fetch_all(query)

@app.post("/todos/{user_id}", response_model=TodoResponse)
async def create_todo(user_id: int, todo: TodoCreate):
    # Check if user exists
    user_query = users.select().where(users.c.id == user_id)
    existing_user = await database.fetch_one(user_query)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    query = todos.insert().values(text=todo.text, completed=todo.completed, user_id=user_id)
    last_record_id = await database.execute(query)
    return {**todo.dict(), "id": last_record_id, "user_id": user_id}

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    # Fetch existing
    query = todos.select().where(todos.c.id == todo_id)
    existing_todo = await database.fetch_one(query)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    update_data = todo_update.dict(exclude_unset=True)
    if not update_data:
        return existing_todo
        
    update_query = todos.update().where(todos.c.id == todo_id).values(**update_data)
    await database.execute(update_query)
    
    updated_query = todos.select().where(todos.c.id == todo_id)
    return await database.fetch_one(updated_query)

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    query = todos.select().where(todos.c.id == todo_id)
    existing_todo = await database.fetch_one(query)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    delete_query = todos.delete().where(todos.c.id == todo_id)
    await database.execute(delete_query)
    return {"message": "Todo deleted successfully"}
