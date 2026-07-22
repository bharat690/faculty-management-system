# Faculty Management System

A web-based Faculty Management System built with **Streamlit** and **PostgreSQL** for **COER University**. The system digitizes daily faculty attendance, activity reporting, availability tracking, and administrative analytics through a centralized dashboard.

> **Status:** Production Deployment
>
> **Live Demo:** https://coer-cosc.streamlit.app/
>
> **Note:** This application is an **internal tool** intended exclusively for authorized COER University faculty and administration.

---

## Overview

The Faculty Management System replaces manual attendance registers and paper-based workload reporting with a centralized digital platform.

Faculty members can:

- Mark daily attendance
- Submit their complete day schedule
- Change their account password

The Dean/Administration can:

- Monitor faculty attendance in real time
- View faculty availability by lecture slot
- Analyze faculty workload and teaching hours
- Manage faculty accounts
- Perform semester resets
- Generate faculty activity summaries

---

## Features

### Faculty Portal

- Secure login
- Daily attendance
- Eight-slot daily activity planner
- Teaching topic logging
- Research/Meeting/Office work tracking
- Password management

---

### Dean Dashboard

- Live attendance statistics
- Faculty availability viewer
- Department-wise filtering
- Current semester monitoring
- Attendance health metrics
- Pending attendance alerts

---

### Faculty Analytics

For every faculty member:

- Weekly summary
- Monthly summary
- Semester summary
- Teaching hours
- Work hours
- Free hours
- Weekly classes
- Topics taught

---

### Administration

- Add faculty
- Bulk faculty upload using CSV
- Faculty management
- Reset passwords
- Delete faculty
- Semester management
- Start new semester

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | PostgreSQL |
| Authentication | bcrypt |
| Data Processing | Pandas |
| Deployment | Streamlit Community Cloud |

---

## Project Structure

```
Directory structure:
└── faculty-management-system/
    ├── README.md
    ├── app.py
    ├── requirements.txt
    ├── assets/
    │   └── styles.css
    ├── components/
    │   ├── __init__.py
    │   ├── attendance_card.py
    │   ├── charts.py
    │   ├── faculty_table.py
    │   ├── metric_cards.py
    │   ├── navbar.py
    │   └── schedule_form.py
    ├── config/
    │   ├── __init__.py
    │   ├── roles.py
    │   └── settings.py
    ├── database/
    │   ├── __init__.py
    │   ├── db.py
    │   ├── migrations.py
    │   ├── schema.sql
    │   └── seed_data.py
    ├── models/
    │   ├── __init__.py
    │   ├── attendance_model.py
    │   ├── schedule_model.py
    │   ├── semester_model.py
    │   ├── subject_model.py
    │   └── user_model.py
    ├── queries/
    │   ├── __init__.py
    │   ├── analytics_queries.py
    │   ├── attendance_queries.py
    │   ├── faculty_queries.py
    │   ├── report_queries.py
    │   ├── schedule_queries.py
    │   └── semester_queries.py
    ├── services/
    │   ├── __init__.py
    │   ├── analytics_service.py
    │   ├── attendance_service.py
    │   ├── auth_service.py
    │   ├── faculty_service.py
    │   ├── report_service.py
    │   ├── schedule_service.py
    │   └── semester_service.py
    ├── utils/
    │   ├── __init__.py
    │   ├── constants.py
    │   ├── helper.py
    │   ├── password_hash.py
    │   ├── session_manager.py
    │   └── validators.py
    ├── .devcontainer/
    │   └── devcontainer.json
    └── .streamlit/
        └── config.toml

```

Architecture follows a layered approach:

```
Streamlit UI
      │
      ▼
Service Layer
      │
      ▼
Query Layer
      │
      ▼
PostgreSQL Database
```

---

## Database

The application uses PostgreSQL and includes tables for:

- Users
- Attendance
- Daily Activity Logs
- Semesters
- Departments
- Subjects
- Academic Units
- Weekly Schedule Templates

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/faculty-management-system.git
```

Move into the project

```bash
cd faculty-management-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
DATABASE_URL=your_postgresql_connection_string
```

Initialize the database

```bash
python database/migrations.py
```

(Optional) Seed sample data

```bash
python database/seed_data.py
```

Run the application

```bash
streamlit run app.py
```

---

## Deployment

The production instance is deployed on Streamlit Cloud.

**Live URL**

https://coer-cosc.streamlit.app/

Database credentials are supplied through Streamlit Secrets in production.

---

## User Roles

### Faculty

- Login
- Mark attendance
- Submit daily schedule
- Change password

### Dean

- Dashboard
- Attendance monitoring
- Faculty availability
- Faculty analytics
- Faculty management
- Semester management

---

## Bulk Upload Format

CSV format:

```csv
employee_id,full_name,email,department,skills
EMP001,John Doe,john@coeruniversity.ac.in,CSE,Python
EMP002,Jane Smith,jane@coeruniversity.ac.in,AI&ML,Machine Learning
```

After upload, the system generates downloadable credentials for all newly created faculty accounts.

---

## Security

- Passwords stored using bcrypt hashing
- Role-based authentication
- Session management
- Password reset functionality
- Password change support

---

## Future Improvements

- Email notifications
- Timetable integration
- Leave management
- Excel/PDF report export
- Department Head dashboard
- Subject allocation module
- Audit logs
- API support
- Dynamic Schedule Form

---

## Author

**Bharat**

B.Tech Computer Science (AI & ML)

COER University

---


This project was developed as an internal software solution for **COER University**.

Unauthorized commercial redistribution or deployment is not permitted without permission from the author and the university.
