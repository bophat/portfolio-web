from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Profile(Base):
    __tablename__ = "profile"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, default="Alex Chen")
    title = Column(String(200), nullable=False, default="Junior Backend & Data Engineer")
    summary = Column(Text)
    hero_badge = Column(String(100), default="Open to opportunities")
    stats_projects = Column(String(20), default="2")
    stats_technologies = Column(String(20), default="4+")
    stats_graduate_year = Column(String(20), default="2024")


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)  # e.g., "Programming Languages"
    category_icon = Column(String(50), default="code")  # icon name
    name = Column(String(100), nullable=False)  # e.g., "Python"
    level = Column(Integer, default=3)  # 1-3 (1=basic, 2=intermediate, 3=comfortable)
    is_learning = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(10), default="01")
    project_type = Column(String(100))  # e.g., "Data Engineering"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    what_learned = Column(Text)  # JSON array stored as text
    tech_tags = Column(Text)  # JSON array stored as text
    github_link = Column(String(500))
    sort_order = Column(Integer, default=0)


class LearningGoal(Base):
    __tablename__ = "learning_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)  # "currently", "6month", "howlearn"
    icon = Column(String(10), default="🎯")
    title = Column(String(200), nullable=False)
    items = Column(Text)  # JSON array stored as text
    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)


class AboutInfo(Base):
    __tablename__ = "about_info"
    
    id = Column(Integer, primary_key=True, index=True)
    paragraphs = Column(Text)  # JSON array of paragraphs
    highlight_text = Column(Text)
    personal_note = Column(Text)


class QuickFact(Base):
    __tablename__ = "quick_facts"
    
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=False)
    value = Column(String(200), nullable=False)
    is_available = Column(Boolean, default=False)  # for highlighting "Available" status
    sort_order = Column(Integer, default=0)


class ContactInfo(Base):
    __tablename__ = "contact_info"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_type = Column(String(50), nullable=False)  # "email", "linkedin", "github"
    label = Column(String(100), nullable=False)
    value = Column(String(200), nullable=False)
    link = Column(String(500))
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
