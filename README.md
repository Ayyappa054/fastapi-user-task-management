# fastapi-user-task-management
FastAPI-LLM-Integration: A FastAPI-based user authentication and task management API with JWT authentication, SQLAlchemy ORM, and LLM integration for dynamic query execution. Supports role-based access control and CRUD operations for efficient user and task management.
FastAPI User Task Management
Overview
FastAPI User Task Management is a high-performance REST API built with FastAPI, featuring JWT-based authentication, SQLAlchemy ORM, and role-based access control (RBAC). The API allows users to manage tasks efficiently while enabling AI-powered query execution using a Large Language Model (LLM) for dynamic queries.

Key Features
✅ User Authentication & Authorization – Secure login with JWT tokens
✅ Role-Based Access Control (RBAC) – Admin/User role management
✅ Task Management System – Perform CRUD operations on tasks
✅ AI-Powered Query Execution – Execute queries via LLM integration
✅ SQLAlchemy ORM – Database management with relational mapping
✅ Dependency Injection & Security – Secure API endpoints with FastAPI’s Depends()
✅ Optimized Performance – Asynchronous operations with FastAPI

Tech Stack
FastAPI – High-performance API framework
SQLAlchemy – ORM for database interactions
JWT Authentication – Secure user authentication
LLM Integration – AI-powered dynamic query execution
PostgreSQL/MySQL – Compatible relational databases
Docker (optional) – Containerization for easy deployment

Installation
1. Clone the Repository
git clone https://github.com/your-username/fastapi-user-task-management.git
cd fastapi-user-task-management
2. Set Up Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Run the FastAPI Server
uvicorn main:app --reload

API Endpoints
🔑 Authentication
POST /login/ → User Login (returns JWT token)

👥 User Management
GET /all_users/ → Retrieve all users
POST /task/users/ → Create a new user
GET /task/{user_id}/ → Get user details
PUT /task/{user_id}/ → Update user details
DELETE /task/{user_id}/ → Delete a user

📝 Task Management
GET /all_tasks/ → Retrieve all tasks
POST /task/tasks/ → Create a new task
GET /task/{task_id}/ → Get a specific task
PUT /task/{task_id}/ → Update task details
DELETE /task/{task_id}/ → Delete a task
🤖 AI-Powered Query Execution
POST /get-Query/ → Execute an LLM-generated query
Security & Role Management
Only Admins can create or delete users.
Users can manage only their assigned tasks.
JWT Authentication ensures secure API access.
