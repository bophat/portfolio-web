# Portfolio Web Application

A full-stack portfolio website built with **FastAPI**, **MySQL**, and **Docker**. Features user authentication, admin panel for content management, and a beautiful responsive design.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## ✨ Features

- **User Authentication**: Register/Login with JWT tokens
- **Admin Panel**: Edit portfolio content without touching code
- **MySQL Database**: Persistent data storage
- **Docker Ready**: One-command deployment
- **Responsive Design**: Modern, beautiful UI
- **API Endpoints**: RESTful API for all content

## 🚀 Quick Start with Docker

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Run the Application

```bash
# Clone the repository
git clone <your-repo-url>
cd portfolio

# Copy environment file
cp .env.example .env

# Start with Docker Compose
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
```

### Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| Portfolio | http://localhost:8000 | Main website |
| Admin Panel | http://localhost:8000/admin | Content management |
| phpMyAdmin | http://localhost:8080 | Database management |

### Default Login

The **first registered user** automatically becomes an admin.

1. Go to http://localhost:8000/register
2. Create an account
3. Login at http://localhost:8000/login
4. Access Admin Panel

## 🛠️ Development Setup

### Without Docker (Local Development)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up MySQL database locally
# Update DATABASE_URL in .env to point to your local MySQL

# Run the application
uvicorn backend.main:app --reload
```

## 📁 Project Structure

```
portfolio/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Authentication logic
│   ├── seed.py           # Database seeder
│   └── routers/          # API routers
│       ├── auth_router.py
│       ├── profile_router.py
│       ├── skills_router.py
│       ├── projects_router.py
│       ├── learning_router.py
│       └── contact_router.py
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── admin/
│       └── dashboard.html
├── static/
│   └── css/
│       └── styles.css
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Profile
- `GET /api/profile/` - Get profile
- `PUT /api/profile/` - Update profile (admin)

### Skills
- `GET /api/skills/` - Get all skills
- `POST /api/skills/` - Create skill (admin)
- `PUT /api/skills/{id}` - Update skill (admin)
- `DELETE /api/skills/{id}` - Delete skill (admin)

### Projects
- `GET /api/projects/` - Get all projects
- `POST /api/projects/` - Create project (admin)
- `PUT /api/projects/{id}` - Update project (admin)
- `DELETE /api/projects/{id}` - Delete project (admin)

## 🗄️ MySQL Workbench Connection

To connect from MySQL Workbench:

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 3306 |
| Username | portfolio_user |
| Password | portfolio_password |
| Database | portfolio_db |

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Remove everything including volumes
docker-compose down -v
```

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | MySQL connection string | mysql+pymysql://... |
| SECRET_KEY | JWT secret key | (change in production!) |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration | 1440 (24 hours) |
| MYSQL_ROOT_PASSWORD | MySQL root password | rootpassword |
| MYSQL_PASSWORD | MySQL user password | portfolio_password |

## 📝 License

MIT License - feel free to use for your own portfolio!

---

Built with ❤️ using FastAPI, MySQL, and Docker
