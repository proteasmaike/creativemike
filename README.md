# Flask Task Management API

A simple yet powerful REST API for managing tasks built with Flask and SQLAlchemy.

## Features

- ✅ Complete CRUD operations for tasks
- ✅ Task filtering by status and priority
- ✅ Task statistics and summary
- ✅ SQLite database integration
- ✅ Docker containerization
- ✅ Health check endpoint
- ✅ Error handling

## Project Structure

. ├── app.py # Main Flask application ├── requirements.txt # Python dependencies ├── Dockerfile # Docker container configuration ├── docker-compose.yml # Docker Compose setup ├── .gitignore # Git ignore rules └── README.md # This file
Code


## Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/proteasmaike/creativemike.git
   cd creativemike

    Create a virtual environment
    bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    Install dependencies
    bash

    pip install -r requirements.txt

    Run the application
    bash

    python app.py

The API will be available at http://localhost:5000
Docker

    Build the Docker image
    bash

    docker build -t flask-task-api .

    Run the container
    bash

    docker run -p 5000:5000 flask-task-api

    Using Docker Compose
    bash

    docker-compose up

API Endpoints
Health Check

    GET /health
        Returns the health status of the API

Tasks
Get All Tasks

    GET /api/tasks
    Query Parameters:
        status (optional): Filter by status (pending, in_progress, completed)
        priority (optional): Filter by priority (low, medium, high)
    Response: List of tasks

Get Single Task

    GET /api/tasks/<task_id>
    Response: Single task object

Create Task

    POST /api/tasks
    Body:
    JSON

    {
      "title": "Buy groceries",
      "description": "Buy milk, eggs, and bread",
      "status": "pending",
      "priority": "medium"
    }

    Response: Created task object

Update Task

    PUT /api/tasks/<task_id>
    Body: Any of the task fields to update
    JSON

    {
      "status": "completed",
      "priority": "high"
    }

    Response: Updated task object

Delete Task

    DELETE /api/tasks/<task_id>
    Response: Success message

Get Task Statistics

    GET /api/tasks/stats/summary
    Response: Task count statistics

Example Usage
Create a Task
bash

curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the Flask API",
    "status": "in_progress",
    "priority": "high"
  }'

Get All Tasks
bash

curl http://localhost:5000/api/tasks

Get Completed Tasks
bash

curl http://localhost:5000/api/tasks?status=completed

Update a Task
bash

curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'

Delete a Task
bash

curl -X DELETE http://localhost:5000/api/tasks/1

Get Statistics
bash

curl http://localhost:5000/api/tasks/stats/summary

Response Format

All API responses follow this format:
JSON

{
  "success": true,
  "data": {}
}

Error responses:
JSON

{
  "success": false,
  "error": "Error message here"
}

Task Model
Code

{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "status": "pending|in_progress|completed",
  "priority": "low|medium|high",
  "created_at": "2026-05-13T10:30:00",
  "updated_at": "2026-05-13T10:30:00"
}

Environment Variables

Create a .env file in the project root:
Code

FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=sqlite:///tasks.db

Technologies Used

    Flask - Lightweight Python web framework
    SQLAlchemy - SQL toolkit and ORM
    SQLite - Lightweight database
    Docker - Containerization

Contributing

Feel free to fork this project and submit pull requests for any improvements!
License

This project is open source and available under the MIT License.
Author

Created by proteasmaike
Support

For issues and questions, please open an issue on the GitHub repository.
