import json
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

def init_db():
    """Create all tables"""
    models.Base.metadata.create_all(bind=engine)

def seed_data(db: Session):
    """Seed initial data if tables are empty"""
    
    # Check if already seeded
    if db.query(models.Profile).first():
        return
    
    # Seed Profile
    profile = models.Profile(
        name="Alex Chen",
        title="Junior Backend & Data Engineer",
        summary="Recent graduate with a strong foundation in Python and SQL. I enjoy building reliable data pipelines and backend services. Currently seeking my first full-time role where I can learn from experienced engineers and contribute to meaningful projects.",
        hero_badge="Open to opportunities",
        stats_projects="2",
        stats_technologies="4+",
        stats_graduate_year="2024"
    )
    db.add(profile)
    
    # Seed Skills
    skills_data = [
        # Programming Languages
        {"category": "Programming Languages", "category_icon": "code", "name": "Python", "level": 3, "sort_order": 0},
        {"category": "Programming Languages", "category_icon": "code", "name": "SQL", "level": 3, "sort_order": 1},
        {"category": "Programming Languages", "category_icon": "code", "name": "JavaScript", "level": 2, "sort_order": 2},
        {"category": "Programming Languages", "category_icon": "code", "name": "Bash scripting", "level": 1, "sort_order": 3},
        # Data & Databases
        {"category": "Data & Databases", "category_icon": "database", "name": "PostgreSQL", "level": 3, "sort_order": 0},
        {"category": "Data & Databases", "category_icon": "database", "name": "MySQL", "level": 3, "sort_order": 1},
        {"category": "Data & Databases", "category_icon": "database", "name": "pandas & NumPy", "level": 2, "sort_order": 2},
        {"category": "Data & Databases", "category_icon": "database", "name": "Basic ETL concepts", "level": 2, "sort_order": 3},
        # Backend & Tools
        {"category": "Backend & Tools", "category_icon": "server", "name": "Flask / FastAPI", "level": 2, "sort_order": 0},
        {"category": "Backend & Tools", "category_icon": "server", "name": "REST API basics", "level": 2, "sort_order": 1},
        {"category": "Backend & Tools", "category_icon": "server", "name": "Git & GitHub", "level": 3, "sort_order": 2},
        {"category": "Backend & Tools", "category_icon": "server", "name": "Docker", "level": 1, "is_learning": True, "sort_order": 3},
        # Concepts & Methods
        {"category": "Concepts & Methods", "category_icon": "book", "name": "Data modeling basics", "level": 2, "sort_order": 0},
        {"category": "Concepts & Methods", "category_icon": "book", "name": "Unit testing", "level": 2, "sort_order": 1},
        {"category": "Concepts & Methods", "category_icon": "book", "name": "Agile/Scrum exposure", "level": 2, "sort_order": 2},
        {"category": "Concepts & Methods", "category_icon": "book", "name": "Technical docs", "level": 2, "sort_order": 3},
    ]
    for skill_data in skills_data:
        db.add(models.Skill(**skill_data))
    
    # Seed Projects
    projects_data = [
        {
            "number": "01",
            "project_type": "Data Engineering",
            "title": "Weather Data Pipeline",
            "description": "A Python script that fetches weather data from a public API daily, cleans and transforms it, then stores it in a PostgreSQL database. Includes a simple dashboard to visualize temperature trends.",
            "what_learned": json.dumps([
                "Working with REST APIs and JSON responses",
                "Data validation and handling edge cases",
                "SQL queries for data aggregation",
                "Scheduling scripts with cron jobs",
                "Importance of logging and error handling"
            ]),
            "tech_tags": json.dumps(["Python", "PostgreSQL", "requests", "pandas", "Matplotlib"]),
            "github_link": "#",
            "sort_order": 0
        },
        {
            "number": "02",
            "project_type": "Backend Development",
            "title": "Task Management API",
            "description": "A RESTful API for managing personal tasks. Users can create, update, delete, and filter tasks by status or due date. Includes user authentication and input validation.",
            "what_learned": json.dumps([
                "Designing REST endpoints and HTTP methods",
                "Database schema design and relationships",
                "Input validation and error responses",
                "Basic authentication with JWT tokens",
                "Writing unit tests for API endpoints"
            ]),
            "tech_tags": json.dumps(["Python", "FastAPI", "SQLAlchemy", "MySQL", "pytest"]),
            "github_link": "#",
            "sort_order": 1
        }
    ]
    for project_data in projects_data:
        db.add(models.Project(**project_data))
    
    # Seed Learning Goals
    learning_goals_data = [
        {
            "category": "currently",
            "icon": "🎯",
            "title": "Currently Learning",
            "items": json.dumps([
                {"title": "Docker & containerization", "description": "Building development environments"},
                {"title": "Cloud basics (AWS)", "description": "EC2, S3, RDS fundamentals"},
                {"title": "DSA Practice", "description": "2-3 LeetCode problems/week"}
            ]),
            "sort_order": 0
        },
        {
            "category": "6month",
            "icon": "🚀",
            "title": "6-Month Goals",
            "items": json.dumps([
                {"title": "Apache Airflow basics", "description": "Workflow orchestration"},
                {"title": "CI/CD pipelines", "description": "GitHub Actions for automation"},
                {"title": "System design fundamentals", "description": "Understanding common patterns"}
            ]),
            "is_featured": True,
            "sort_order": 1
        },
        {
            "category": "howlearn",
            "icon": "💡",
            "title": "How I Learn Best",
            "items": json.dumps([
                {"title": "Building projects", "description": "Hands-on implementation"},
                {"title": "Code reviews", "description": "Learning from feedback"},
                {"title": "Documentation", "description": "Reading official docs first"}
            ]),
            "sort_order": 2
        }
    ]
    for goal_data in learning_goals_data:
        db.add(models.LearningGoal(**goal_data))
    
    # Seed About Info
    about = models.AboutInfo(
        paragraphs=json.dumps([
            "I graduated in 2024 with a degree in Computer Science. During my studies, I discovered I enjoy working with data — there's something satisfying about taking messy inputs and turning them into clean, useful information.",
            "I don't have professional experience yet, but I've spent the past year building personal projects and learning through online courses. I'm most comfortable with Python and SQL, and I'm working to expand my knowledge of cloud services and data tools."
        ]),
        highlight_text="What I'm looking for: A team that values learning and isn't afraid to give juniors real work. I'm eager to contribute, ask questions, and grow into a reliable engineer over time.",
        personal_note="Outside of coding, I enjoy hiking and playing chess (badly). 🏔️ ♟️"
    )
    db.add(about)
    
    # Seed Quick Facts
    quick_facts_data = [
        {"label": "Location", "value": "Open to remote or relocating", "sort_order": 0},
        {"label": "Education", "value": "B.S. Computer Science, 2024", "sort_order": 1},
        {"label": "Languages", "value": "English (fluent)", "sort_order": 2},
        {"label": "Availability", "value": "Immediately", "is_available": True, "sort_order": 3},
    ]
    for fact_data in quick_facts_data:
        db.add(models.QuickFact(**fact_data))
    
    # Seed Contact Info
    contact_data = [
        {"contact_type": "email", "label": "Email", "value": "alex.chen@email.com", "link": "mailto:alex.chen@email.com", "icon": "mail", "sort_order": 0},
        {"contact_type": "linkedin", "label": "LinkedIn", "value": "linkedin.com/in/alexchen", "link": "https://linkedin.com/in/alexchen", "icon": "linkedin", "sort_order": 1},
        {"contact_type": "github", "label": "GitHub", "value": "github.com/alexchen", "link": "https://github.com/alexchen", "icon": "github", "sort_order": 2},
    ]
    for contact in contact_data:
        db.add(models.ContactInfo(**contact))
    
    db.commit()
    print("Database seeded successfully!")

def run_seed():
    """Run the seeder"""
    init_db()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
