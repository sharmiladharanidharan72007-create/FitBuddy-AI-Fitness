# 💪 FitBuddy – AI Fitness Plan Generator


## 📌 Project Overview

FitBuddy is an AI-powered fitness and wellness web application that generates personalized 7-day workout and food plans using Google Gemini AI.

The application collects basic user information such as name, age, weight, fitness goal, workout intensity, and optional health information.

Based on these details, FitBuddy generates a personalized fitness plan containing:

- 🏋️ 7-day workout plan
- 🥗 7-day food plan
- 💧 Nutrition and recovery tips
- ❤️ Health-aware workout considerations
- 🔄 Feedback-based plan updates

---

# 1. 📚 Prerequisites

Before developing FitBuddy, the following software and technologies are required:

### Software

- Python 3.x
- Visual Studio Code
- Git
- GitHub
- Web browser

### Technologies

- Python
- FastAPI
- Uvicorn
- Jinja2
- SQLAlchemy
- SQLite
- HTML
- CSS
- Google Gemini API

### Python Libraries

```text
fastapi
uvicorn[standard]
jinja2
sqlalchemy
python-multipart
google-genai
python-dotenv
pydantic
2. 🔄 Project Workflow
The FitBuddy application follows this workflow:
User
  ↓
Enter Personal Information
  ↓
Select Fitness Goal
  ↓
Select Workout Intensity
  ↓
Enter Optional Health Information
  ↓
FastAPI Backend
  ↓
Google Gemini AI
  ↓
Generate 7-Day Workout Plan
  ↓
Generate 7-Day Food Plan
  ↓
Display Personalized Result
  ↓
User Provides Feedback
  ↓
Gemini Updates the Plan
  ↓
Updated Fitness Plan
3. 🧠 Model Selection and Architecture
FitBuddy uses Google Gemini models for AI-based fitness plan generation.
Main AI Model
The main Gemini model is used to generate:
Personalized workouts
7-day food plans
Health-aware modifications
Fitness recommendations
Feedback-based plan updates
Gemini Flash
Gemini Flash is used for short nutrition and recovery tips.
Architecture
                ┌─────────────────────┐
                │       User          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   HTML / Jinja2     │
                │      Frontend       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      FastAPI        │
                │      Backend        │
                └───────┬─────┬───────┘
                        │     │
              ┌─────────┘     └─────────┐
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │ Google Gemini│          │    SQLite    │
       │      AI      │          │   Database   │
       └──────────────┘          └──────────────┘
4. 🏗️ Define the Application Architecture
FitBuddy follows a simple layered architecture.
Frontend Layer
The frontend is developed using:
HTML
CSS
Jinja2 templates
Backend Layer
The backend is developed using:
Python
FastAPI
AI Layer
Google Gemini is responsible for generating personalized fitness plans.
Database Layer
SQLite and SQLAlchemy are used to store:
User information
Fitness plans
Feedback
Updated plans
5. 💻 Set Up the Development Environment
Create Project Folder
FitBuddy-AI-Fitness
Create Virtual Environment
python -m venv venv
Activate Virtual Environment
Windows:
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Environment Variable
Create a .env file:
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
The API key should never be uploaded to GitHub.
6. ⚙️ Develop the Core Functionalities
The main functionalities of FitBuddy include:
User Input
The application collects:
Name
User ID
Age
Weight
Fitness Goal
Workout Intensity
Health Information
AI Fitness Plan
Gemini generates a personalized 7-day plan.
Food Plan
The AI automatically generates food suggestions for:
Breakfast
Lunch
Evening Snack
Dinner
Health-Aware Planning
The user's reported health information is considered while generating the workout.
Feedback
Users can provide feedback about their plan.
Example:
The workout is too difficult.
Please make it easier.
The AI then generates an updated plan.
7. 🚀 Implement the FastAPI Backend
FastAPI is used to create the backend application.
Main Routes
GET  /
POST /generate-workout
POST /submit-feedback
GET  /view-all-users
GET  /api/users
GET  /docs
Main Backend Components
app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routes.py
├── gemini_generator.py
├── gemini_flash_generator.py
└── updated_plan.py
8. 🐍 Main Application Development
The main FastAPI application is created in:
app/main.py
It is responsible for:
Creating the FastAPI application
Loading routes
Serving static files
Initializing the database
The application is started using:
uvicorn app.main:app --reload
The local application can then be accessed at:
http://127.0.0.1:8000
9. 🎨 Frontend Development
The FitBuddy frontend provides a simple and attractive interface.
First Page
The first page allows the user to enter their fitness information.
It contains:
FitBuddy branding
Name
User ID
Age
Weight
Fitness goal
Workout intensity
Health information
Generate Plan button
Second Page
The result page displays:
User profile
Health consideration
7-day workout plan
7-day food plan
Nutrition/recovery tip
Feedback form
Plan update button
10. 📄 Creating Dynamic Templates
Jinja2 is used to create dynamic HTML pages.
Templates
templates/
│
├── index.html
├── result.html
└── all_users.html
The backend sends data to the templates.
For example:
Username
Age
Weight
Goal
Intensity
Health Problem
Workout Plan
Nutrition Tip
The result page dynamically displays the AI-generated plan.
11. ☁️ Preparing the Application for Deployment
Before deployment, the application must be prepared for production.
Deployment Requirements
GitHub repository
requirements.txt
FastAPI application
Environment variables
Gemini API key
Production server command
The project can be deployed using a cloud hosting platform such as Render.
The production application should use an appropriate start command such as:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
The Gemini API key should be added through the hosting platform's environment variables.
12. 🧪 Testing and Verifying Local Deployment
The application should be tested before deployment.
Test the Application
Run:
uvicorn app.main:app --reload
Open:
http://127.0.0.1:8000
Test User Input
Example:
Name: Sharmila D
User ID: FB001
Age: 19
Weight: 50
Fitness Goal: General Wellness
Workout Intensity: Medium
Health Problem: No problem
Verify
Check that:
User information is accepted
Gemini generates the fitness plan
7 days are displayed
Food suggestions are generated
Nutrition tip is displayed
Health information is considered
Feedback can be submitted
The plan is updated
Data is stored in SQLite
13. ✅ Conclusion
FitBuddy demonstrates how Generative AI can be integrated into a web application to create personalized fitness and wellness plans.
The project combines:
Python
FastAPI
Google Gemini AI
SQLite
SQLAlchemy
Jinja2
HTML
CSS
The application provides an interactive workflow where users can enter their information, receive an AI-generated 7-day fitness and food plan, and provide feedback to improve the plan.
FitBuddy is designed as an educational and general wellness application.
📁 Project Structure
FitBuddy-AI-Fitness/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
│
├── static/
│   └── style.css
│
├── requirements.txt
├── README.md
└── .env
▶️ Run the Project
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Open:
http://127.0.0.1:8000
API documentation:
http://127.0.0.1:8000/docs


