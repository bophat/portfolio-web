import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
import json

from .database import engine, get_db, SessionLocal
from . import models, auth
from .routers import (
    auth_router,
    profile_router,
    skills_router,
    projects_router,
    learning_router,
    contact_router,
)
from .seed import init_db, seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Create tables and seed data
    init_db()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
    yield
    # Shutdown: Nothing to do


app = FastAPI(
    title="Portfolio API",
    description="API for managing portfolio content",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Register API routers
app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(skills_router.router)
app.include_router(projects_router.router)
app.include_router(learning_router.router)
app.include_router(contact_router.router)


# Helper to get current user from cookie
async def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    """Get current user from cookie token"""
    token = request.cookies.get("access_token")
    if token and token.startswith("Bearer "):
        token = token[7:]
        try:
            from jose import jwt
            from .config import settings
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if username:
                return auth.get_user_by_username(db, username)
        except:
            pass
    return None


# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


# Main page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Render the main portfolio page"""
    current_user = await get_current_user_from_cookie(request, db)
    
    # Get all data from database
    profile = db.query(models.Profile).first()
    skills = db.query(models.Skill).order_by(models.Skill.category, models.Skill.sort_order).all()
    projects = db.query(models.Project).order_by(models.Project.sort_order).all()
    learning_goals = db.query(models.LearningGoal).order_by(models.LearningGoal.sort_order).all()
    about = db.query(models.AboutInfo).first()
    quick_facts = db.query(models.QuickFact).order_by(models.QuickFact.sort_order).all()
    contacts = db.query(models.ContactInfo).order_by(models.ContactInfo.sort_order).all()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = {
                "name": skill.category,
                "icon": skill.category_icon,
                "skills": []
            }
        skills_by_category[skill.category]["skills"].append(skill)
    
    # Parse JSON fields
    for project in projects:
        if project.what_learned:
            project.what_learned_list = json.loads(project.what_learned)
        else:
            project.what_learned_list = []
        if project.tech_tags:
            project.tech_tags_list = json.loads(project.tech_tags)
        else:
            project.tech_tags_list = []
    
    for goal in learning_goals:
        if goal.items:
            goal.items_list = json.loads(goal.items)
        else:
            goal.items_list = []
    
    if about and about.paragraphs:
        about.paragraphs_list = json.loads(about.paragraphs)
    else:
        about = models.AboutInfo()
        about.paragraphs_list = []
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "current_user": current_user,
        "profile": profile,
        "skills_categories": list(skills_by_category.values()),
        "projects": projects,
        "learning_goals": learning_goals,
        "about": about,
        "quick_facts": quick_facts,
        "contacts": contacts
    })


# Login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    """Render login page"""
    current_user = await get_current_user_from_cookie(request, db)
    if current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


# Register page
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)):
    """Render register page"""
    current_user = await get_current_user_from_cookie(request, db)
    if current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("register.html", {"request": request})


# Admin dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Render admin dashboard"""
    current_user = await get_current_user_from_cookie(request, db)
    if not current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login", status_code=302)
    
    profile = db.query(models.Profile).first()
    skills = db.query(models.Skill).order_by(models.Skill.category, models.Skill.sort_order).all()
    projects = db.query(models.Project).order_by(models.Project.sort_order).all()
    learning_goals = db.query(models.LearningGoal).order_by(models.LearningGoal.sort_order).all()
    quick_facts = db.query(models.QuickFact).order_by(models.QuickFact.sort_order).all()
    contacts = db.query(models.ContactInfo).order_by(models.ContactInfo.sort_order).all()
    
    # Parse JSON fields for display
    for project in projects:
        if project.what_learned:
            project.what_learned_list = json.loads(project.what_learned)
        else:
            project.what_learned_list = []
        if project.tech_tags:
            project.tech_tags_list = json.loads(project.tech_tags)
        else:
            project.tech_tags_list = []
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "learning_goals": learning_goals,
        "quick_facts": quick_facts,
        "contacts": contacts
    })
