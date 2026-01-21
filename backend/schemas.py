from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============ User Schemas ============
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ============ Profile Schemas ============
class ProfileBase(BaseModel):
    name: str
    title: str
    summary: Optional[str] = None
    hero_badge: Optional[str] = "Open to opportunities"
    stats_projects: Optional[str] = "2"
    stats_technologies: Optional[str] = "4+"
    stats_graduate_year: Optional[str] = "2024"


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    name: Optional[str] = None
    title: Optional[str] = None


class ProfileResponse(ProfileBase):
    id: int
    
    class Config:
        from_attributes = True


# ============ Skill Schemas ============
class SkillBase(BaseModel):
    category: str
    category_icon: Optional[str] = "code"
    name: str
    level: Optional[int] = 3
    is_learning: Optional[bool] = False
    sort_order: Optional[int] = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    category: Optional[str] = None
    category_icon: Optional[str] = None
    name: Optional[str] = None
    level: Optional[int] = None
    is_learning: Optional[bool] = None
    sort_order: Optional[int] = None


class SkillResponse(SkillBase):
    id: int
    
    class Config:
        from_attributes = True


# ============ Project Schemas ============
class ProjectBase(BaseModel):
    number: Optional[str] = "01"
    project_type: Optional[str] = None
    title: str
    description: Optional[str] = None
    what_learned: Optional[str] = None  # JSON string
    tech_tags: Optional[str] = None  # JSON string
    github_link: Optional[str] = None
    sort_order: Optional[int] = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    number: Optional[str] = None
    project_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    what_learned: Optional[str] = None
    tech_tags: Optional[str] = None
    github_link: Optional[str] = None
    sort_order: Optional[int] = None


class ProjectResponse(ProjectBase):
    id: int
    
    class Config:
        from_attributes = True


# ============ Learning Goal Schemas ============
class LearningGoalBase(BaseModel):
    category: str  # "currently", "6month", "howlearn"
    icon: Optional[str] = "🎯"
    title: str
    items: Optional[str] = None  # JSON string
    is_featured: Optional[bool] = False
    sort_order: Optional[int] = 0


class LearningGoalCreate(LearningGoalBase):
    pass


class LearningGoalUpdate(BaseModel):
    category: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None
    items: Optional[str] = None
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None


class LearningGoalResponse(LearningGoalBase):
    id: int
    
    class Config:
        from_attributes = True


# ============ About Info Schemas ============
class AboutInfoBase(BaseModel):
    paragraphs: Optional[str] = None  # JSON string
    highlight_text: Optional[str] = None
    personal_note: Optional[str] = None


class AboutInfoCreate(AboutInfoBase):
    pass


class AboutInfoUpdate(AboutInfoBase):
    pass


class AboutInfoResponse(AboutInfoBase):
    id: int
    
    class Config:
        from_attributes = True


# ============ Quick Fact Schemas ============
class QuickFactBase(BaseModel):
    label: str
    value: str
    is_available: Optional[bool] = False
    sort_order: Optional[int] = 0


class QuickFactCreate(QuickFactBase):
    pass


class QuickFactUpdate(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    is_available: Optional[bool] = None
    sort_order: Optional[int] = None


class QuickFactResponse(QuickFactBase):
    id: int
    
    class Config:
        from_attributes = True


# ============ Contact Info Schemas ============
class ContactInfoBase(BaseModel):
    contact_type: str  # "email", "linkedin", "github"
    label: str
    value: str
    link: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = 0


class ContactInfoCreate(ContactInfoBase):
    pass


class ContactInfoUpdate(BaseModel):
    contact_type: Optional[str] = None
    label: Optional[str] = None
    value: Optional[str] = None
    link: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None


class ContactInfoResponse(ContactInfoBase):
    id: int
    
    class Config:
        from_attributes = True
