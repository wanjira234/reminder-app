# Roadmap Reminder App

A Python-based reminder application that helps you track and get reminded about your 2025 roadmap tasks.

## Features

- Store and manage your roadmap tasks
- Get email reminders for upcoming tasks
- Track progress and status of tasks
- Web interface for task management
- Secure authentication

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your email settings:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-specific-password
   EMAIL_FROM=your-email@gmail.com
   EMAIL_TO=your-email@gmail.com
   SECRET_KEY=your-secret-key
   ```
5. Initialize the database:
   ```bash
   python init_db.py
   ```
6. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

1. Access the web interface at `http://localhost:8000`
2. Log in with your credentials
3. Add, edit, or delete tasks
4. Set reminder times for tasks
5. View your progress and upcoming tasks

## API Endpoints

- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/` - List all tasks
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task

## Security

- Uses JWT for authentication
- Passwords are hashed using bcrypt
- Email credentials are stored securely in environment variables 