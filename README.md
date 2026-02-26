# API Dashboard

## Overview

API Dashboard is a backend-driven application designed to manage, expose, and monitor API endpoints through a structured and scalable architecture.

The project demonstrates:

RESTful API design
Database integration
ORM usage
Asynchronous request handling
Clean project structure
Version control workflow
This project is currently under active development.

## What It Does

The API Dashboard:

Exposes REST API endpoints (GET, POST, etc.)
Connects to a relational database (SQLite)
Stores and retrieves structured data
Uses an ORM to map Python classes to database tables
Handles HTTP status codes properly (200, 404, 500, etc.)
Separates concerns (models, routes, database config)

In short:
It acts as a backend service that can create, read, update, and delete resources through structured API endpoints.

## Tech Stack

### Backend

Python 3.x
FastAPI (web framework)
SQLAlchemy (ORM)
SQLite (database)

### Dev Tools

Git (version control)
GitHub (remote repository)
Uvicorn (ASGI server)

## Architecture Overview

The project follows a layered structure:

Client → FastAPI Routes → Business Logic → SQLAlchemy ORM → SQLite Database

### Flow of a Request

Client sends a request (GET /items)
FastAPI receives the request
Route function executes
Database session is opened
SQLAlchemy interacts with SQLite
Response is returned with appropriate status code

## Key Concepts Used

### connect_args={"check_same_thread": False}

SQLite normally restricts connections to one thread.

This setting allows the database connection to be used across multiple threads — which is required when running FastAPI with an async server like Uvicorn.

Without this, you'd get threading errors.

### autocommit=False

Changes are NOT automatically saved to the database.

You must explicitly call commit().

This prevents accidental writes and gives you control.

### autoflush=False

Prevents SQLAlchemy from automatically pushing pending changes to the database before queries.

You decide when to flush changes.

### declarative_base()

Creates a base class for all database models.

Every model (table) inherits from this base.

This allows SQLAlchemy to:

Track models
Create tables automatically
Map Python classes to database tables

### models.Base.metadata.create_all(bind=engine)

This command:

Scans all defined models
Creates tables in the database
Only creates tables that do not already exist

It does NOT delete existing tables.

Think of it as:
“Make sure the database matches my models.”

## HTTP Methods Used

## GET

Retrieve data.

## POST

Create new data.

## PUT / PATCH

Update data.

## DELETE

Remove data.

## HTTP Status Codes

200 → Success
201 → Created
400 → Bad Request
404 → Not Found
500 → Server Error

These help clients understand what happened.

## Async & Await Explained

FastAPI is built for asynchronous performance.

### async

Marks a function as asynchronous.

It allows the server to handle other requests while waiting for slow operations (like database calls or external APIs).

## await

Used inside async functions.

It pauses execution of that function until a task finishes — without blocking the entire server.

Without async/await:

Requests are handled one at a time.
The server waits.

With async/await:

Requests are handled concurrently.
The server stays responsive.

That’s scalability.

## Database Layer

SQLite is used as a lightweight relational database.

SQLAlchemy acts as the abstraction layer between Python and SQL.

Instead of writing raw SQL:

You define models as classes.
SQLAlchemy translates them into SQL queries.
This keeps the code clean and portable.

## Project Structure (Typical)

```bash
api-dashboard/
│
├── main.py          # Entry point
├── models.py        # Database models
├── database.py      # DB configuration
├── routes/          # API endpoints
├── requirements.txt
└── README.md
```

Separation = clarity.

## Current Status

The project is functional at the API level but still evolving.

Planned improvements may include:

Authentication layer
Role-based access control
Dashboard frontend
API logging & monitoring
Environment-based configuration
Migration system (Alembic)
