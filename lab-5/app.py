
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from passlib.context import CryptContext
from db import database, engine, metadata
from models import users
from schema import UserCreate, UserLogin

# Create tables if they don't exist
metadata.create_all(engine)

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login - Auth System</title>
<style>
body { margin: 0; }
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #ffffff;
  font-family: Arial, sans-serif;
  color: #000000;
}
.auth-form-container {
  background-color: #ffffff;
  border: 1px solid #000000;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
}
.auth-form-container h2 {
  text-align: left;
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-weight: normal;
}
.auth-form {
  display: flex;
  flex-direction: column;
}
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}
.form-group label {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
.form-group input {
  padding: 0.5rem;
  border: 1px solid #000000;
  font-size: 1rem;
  outline: none;
  background: transparent;
  box-shadow: none !important;
}
.form-group input:focus {
  border-width: 2px;
}
.submit-btn {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #000000;
  color: #ffffff;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: none !important;
}
.toggle-btn {
  margin-top: 1rem;
  background: transparent;
  border: none;
  color: #000000;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
  text-align: left;
  padding: 0;
  box-shadow: none !important;
}
.msg {
    margin-top: 1rem;
    font-size: 0.9rem;
    text-align: center;
    padding: 0.75rem;
    border: 1px solid transparent;
    display: none;
}
.msg.success {
    display: block;
    border-color: #aaa;
    background-color: #eee;
    color: #333;
}
.msg.error {
    display: block;
    border-color: #999;
    background-color: #fff;
    color: #000;
    font-weight: bold;
}
</style>
</head>
<body>
<div class="app-container">
  <div class="auth-form-container">
    <h2>Login</h2>
    <form class="auth-form" id="loginForm">
      <div class="form-group">
        <label>Username</label>
        <input type="text" id="username" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" id="password" required />
      </div>
      <button type="submit" class="submit-btn">Login</button>
    </form>
    <button type="button" class="toggle-btn" onclick="window.location.href='/register'">
      Register new account
    </button>
    <div id="msgBox" class="msg"></div>
  </div>
</div>
<script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const msgBox = document.getElementById('msgBox');

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            
            if (!response.ok) {
                msgBox.textContent = data.detail || 'An error occurred';
                msgBox.className = 'msg error';
            } else {
                msgBox.textContent = data.message || 'Login successful';
                msgBox.className = 'msg success';
            }
        } catch (error) {
            msgBox.textContent = 'Network error';
            msgBox.className = 'msg error';
        }
    });
</script>
</body>
</html>"""

REGISTER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Register - Auth System</title>
<style>
body { margin: 0; }
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #ffffff;
  font-family: Arial, sans-serif;
  color: #000000;
}
.auth-form-container {
  background-color: #ffffff;
  border: 1px solid #000000;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
}
.auth-form-container h2 {
  text-align: left;
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-weight: normal;
}
.auth-form {
  display: flex;
  flex-direction: column;
}
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}
.form-group label {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
.form-group input {
  padding: 0.5rem;
  border: 1px solid #000000;
  font-size: 1rem;
  outline: none;
  background: transparent;
  box-shadow: none !important;
}
.form-group input:focus {
  border-width: 2px;
}
.submit-btn {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #000000;
  color: #ffffff;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: none !important;
}
.toggle-btn {
  margin-top: 1rem;
  background: transparent;
  border: none;
  color: #000000;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
  text-align: left;
  padding: 0;
  box-shadow: none !important;
}
.msg {
    margin-top: 1rem;
    font-size: 0.9rem;
    text-align: center;
    padding: 0.75rem;
    border: 1px solid transparent;
    display: none;
}
.msg.success {
    display: block;
    border-color: #aaa;
    background-color: #eee;
    color: #333;
}
.msg.error {
    display: block;
    border-color: #999;
    background-color: #fff;
    color: #000;
    font-weight: bold;
}
</style>
</head>
<body>
<div class="app-container">
  <div class="auth-form-container">
    <h2>Register</h2>
    <form class="auth-form" id="registerForm">
      <div class="form-group">
        <label>Username</label>
        <input type="text" id="username" required />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" id="email" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" id="password" required />
      </div>
      <button type="submit" class="submit-btn">Register</button>
    </form>
    <button type="button" class="toggle-btn" onclick="window.location.href='/login'">
      Login again
    </button>
    <div id="msgBox" class="msg"></div>
  </div>
</div>
<script>
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const msgBox = document.getElementById('msgBox');

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            
            if (!response.ok) {
                msgBox.textContent = data.detail || 'An error occurred';
                msgBox.className = 'msg error';
            } else {
                msgBox.textContent = data.message || 'Register successful';
                msgBox.className = 'msg success';
            }
        } catch (error) {
            msgBox.textContent = 'Network error';
            msgBox.className = 'msg error';
        }
    });
</script>
</body>
</html>"""

app = FastAPI()

from fastapi.responses import RedirectResponse

@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url="/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    return HTMLResponse(content=LOGIN_HTML, status_code=200)

@app.get("/register", response_class=HTMLResponse)
async def get_register():
    return HTMLResponse(content=REGISTER_HTML, status_code=200)

# Add CORS so the frontend can easily communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

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
    await database.execute(query)
    
    return {"message": "User registered successfully"}

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
        
    return {"message": "Login successful"}
