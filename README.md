# 💪 FitBuddy – AI Fitness Plan Generator

## 📌 Project Overview

FitBuddy is an AI-powered fitness and wellness web application that generates personalized 7-day workout and food plans using Google Gemini AI.

The application collects basic user information such as:

- Name
- User ID
- Age
- Weight
- Fitness Goal
- Workout Intensity
- Health Information

Based on the user's details, FitBuddy generates a personalized fitness plan and provides health-aware workout suggestions.

Users can also provide feedback, and the AI can update the fitness plan according to their requirements.

---

## 🎯 Project Objectives

- Generate personalized 7-day workout plans.
- Generate personalized 7-day food plans.
- Use Google Gemini AI for intelligent plan generation.
- Consider user-provided health information.
- Allow users to update plans through feedback.
- Provide a simple and user-friendly web interface.
- Store user and fitness plan information securely.
- Demonstrate the practical application of Generative AI.
- ## ✨ Key Features

### 👤 User Profile
- Enter name and user ID.
- Enter age and weight.
- Select fitness goal.
- Select workout intensity.
- Enter optional health information.

### 🏋️ Personalized Workout Plan
- Generates a 7-day workout plan.
- Provides warm-up and cool-down activities.
- Includes exercises, duration, sets, repetitions, and rest periods.
- Adjusts the plan according to the selected fitness goal and intensity.

### 🥗 Personalized Food Plan
- Generates a 7-day food plan.
- Provides breakfast, lunch, evening snack, and dinner.
- Suggests practical and varied food options.
- Considers the user's fitness goal.

### ❤️ Health-Aware Planning
- Accepts different health problems or physical limitations.
- Considers the reported information while generating the workout.
- Can adjust exercises, intensity, duration, and rest.
- Provides general wellness guidance.

### 🔄 Feedback-Based Plan Updates
- Users can provide feedback about their fitness plan.
- Gemini AI processes the feedback.
- The existing plan is modified based on the user's requirements.
- The updated plan is displayed on the result page.
- ## 🛠️ Technologies Used

### Programming Language
- Python

### Frontend
- HTML5
- CSS3
- Jinja2 Templates

### Backend
- FastAPI
- Uvicorn

### Artificial Intelligence
- Google Gemini AI
- Gemini 2.5 Pro
- Gemini 2.5 Flash

### Database
- SQLite
- SQLAlchemy

### Development Tools
- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

### Environment Management
- Python-dotenv
- `.env` file for API key configuration
- ## 🔄 Project Workflow

1. User opens the FitBuddy application.
2. User enters personal and fitness information.
3. User provides optional health information.
4. The information is sent to the FastAPI backend.
5. FastAPI validates and processes the user input.
6. Google Gemini AI generates a personalized 7-day workout and food plan.
7. The generated plan is stored in the SQLite database.
8. The personalized plan is displayed on the result page.
9. User can provide feedback about the generated plan.
10. Gemini AI processes the feedback.
11. The existing plan is updated according to the feedback.
12. The updated plan is displayed to the user.

### Workflow

User Input  
↓  
FastAPI Backend  
↓  
Input Validation  
↓  
Google Gemini AI  
↓  
7-Day Workout & Food Plan  
↓  
SQLite Database  
↓  
Result Page  
↓  
User Feedback  
↓  
AI Plan Update  
↓  
Updated Fitness Plan
## 🏗️ System Architecture

FitBuddy follows a simple client-server architecture.

### Architecture Components

1. **Frontend**
   - HTML
   - CSS
   - Jinja2 Templates
   - Collects user information
   - Displays the generated fitness plan

2. **FastAPI Backend**
   - Handles user requests
   - Validates input data
   - Connects the frontend with the AI model
   - Manages application routes

3. **Google Gemini AI**
   - Generates personalized workout plans
   - Generates food plans
   - Considers health information
   - Updates plans based on user feedback

4. **SQLite Database**
   - Stores user information
   - Stores generated fitness plans
   - Stores feedback
   - Stores updated plans

### Architecture Flow

```text
User
  ↓
HTML / CSS / Jinja2
  ↓
FastAPI Backend
  ↓
Google Gemini AI
  ↓
Personalized Fitness Plan
  ↓
SQLite Database
  ↓
Result Page
## 📂 Project Structure

```text
FitBuddy-AI-Fitness/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
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
└── fitbuddy.db
## ⚙️ Installation and Setup

### Prerequisites

Before installing FitBuddy, make sure the following are installed:

- Python 3.10 or later
- Visual Studio Code
- Git
- Internet connection
- Google Gemini API Key
### 1. Clone the Repository

Open Command Prompt or PowerShell and run:

```bash
git clone https://github.com/sharmiladharanidharan72007-create/FitBuddy-AI-Fitness.git
### 2. Open the Project Folder

Navigate to the cloned project folder:

```bash
cd FitBuddy-AI-Fitness
### 3. Create a Virtual Environment

Create a Python virtual environment for the project:

```bash
python -m venv venv
### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
### 5. Install Required Packages

Install all required Python packages using:

```bash
pip install -r requirements.txt
### 6. Configure the Gemini API Key

Create a file named `.env` in the project root directory.

Add the following:

```text
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
### 7. Run the Application

Start the FastAPI server using:

```bash
uvicorn app.main:app --reload
### 8. Open the Application

After starting the FastAPI server, open a web browser and visit:

```text
http://127.0.0.1:8000
### 9. Open API Documentation

FastAPI provides interactive API documentation.

Open the following URL in your browser:

http://127.0.0.1:8000/docs

The API documentation allows you to view and test the available API endpoints.
### ⚠️ Security Note

- Never upload the `.env` file to GitHub.
- Never share your Gemini API key publicly.
- Store the API key using environment variables.
- Add `.env` to `.gitignore` to prevent accidental upload.
