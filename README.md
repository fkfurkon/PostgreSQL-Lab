# PostgreSQL-Lab

## Description
This project is a Flask-based web application for managing notes with tag support, using PostgreSQL as the database backend. It demonstrates CRUD operations, tag management, and integration with Docker for easy setup.

## Features
- Create, edit, and delete notes
- Assign tags to notes
- View notes by tag
- PostgreSQL database integration
- Docker Compose setup for database and pgAdmin

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd PostgreSQL-Lab
   ```
2. **Start services with Docker Compose:**
   ```bash
   docker-compose up -d
   ```
3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Flask app:**
   ```bash
   cd psunote
   python noteapp.py
   ```

## Usage
- Access the app at `http://localhost:5000`
- Use pgAdmin at `http://localhost:7080` (default email: coe@local.db, password: CoEpasswd)

## Folder Structure
- `psunote/` - Main Flask app and templates
- `docker-compose.yml` - Docker setup for PostgreSQL and pgAdmin
- `requirements.txt` - Python dependencies

## License
MIT