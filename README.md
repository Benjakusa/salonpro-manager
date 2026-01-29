# SalonPro Manager – CLI Salon Management System

## Project Overview

SalonPro Manager is a Command Line Interface (CLI) application designed to help small and medium-sized hair salons manage daily operations efficiently. It addresses common challenges such as double booking, lack of client history tracking, and unstructured stylist scheduling.

### Problem Statement

Small salons often struggle with:

- Paper appointment books leading to double booking
- Spreadsheets that do not track client history effectively
- No centralized system for managing stylist schedules
- Manual service and revenue tracking

### Solution

SalonPro Manager provides:

- Centralized management for clients, stylists, services, and appointments
- Scheduling conflict detection to prevent double booking
- Complete client appointment history
- Stylist availability and scheduling
- Revenue and performance insights

---

## Features

### Core Functionality

- **Client Management**  
  Add, view, update, and delete clients with full contact details

- **Stylist Management**  
  Manage stylist profiles, specialties, and schedules

- **Service Management**  
  Create and manage salon services with pricing and duration

- **Appointment System**  
  Schedule, modify, cancel, and track appointments with conflict prevention

### Advanced Features

- **Search and Filtering**  
  Search clients by name or phone and filter appointments by date

- **Reports and Analytics**  
  Daily revenue, service popularity, and stylist performance reports

- **Data Validation**  
  Phone number, email, and scheduling conflict validation

- **Relational Data Model**  
  One-to-many relationships across all major entities

---

## Project Structure

salonpro-manager/
├── Pipfile
├── Pipfile.lock
├── README.md
├── salonpro.db
└── lib/
├── cli.py
├── debug.py
├── seed.py
├── test_models.py
├── database/
│ └── init.py
└── models/
├── init.py
├── client.py
├── stylist.py
├── service.py
└── appointment.py

yaml
Copy code

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Pipenv

### Step 1: Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd salonpro-manager
pipenv install
pipenv shell
Step 2: Initialize the Database
bash
Copy code
python lib/debug.py
Or run the CLI directly:

bash
Copy code
python lib/cli.py
Step 3: Seed Sample Data (Optional)
bash
Copy code
python lib/seed.py
Usage
Start the Application
bash
Copy code
python lib/cli.py
Main Menu
markdown
Copy code
MAIN MENU
----------------------------------------
1. Client Management
2. Stylist Management
3. Service Management
4. Appointment Management
5. Reports and Analytics
6. Search and Find
0. Exit Program
----------------------------------------
Example Workflow
Add a client: Main Menu → Client Management → Add Client

Add a stylist: Main Menu → Stylist Management → Add Stylist

Add a service: Main Menu → Service Management → Add Service

Schedule an appointment: Appointment Management → Schedule Appointment

View today's appointments: Appointment Management → Today's Appointments

Database Models
Client Model
text
Copy code
Properties:
- id, first_name, last_name, phone, email, notes

Relationships:
- One Client → Many Appointments

Methods:
- create(), get_all(), find_by_id(), update(), delete()
Stylist Model
text
Copy code
Properties:
- id, first_name, last_name, phone, email, specialty, hourly_rate

Relationships:
- One Stylist → Many Appointments

Methods:
- create(), get_all(), find_by_specialty(), get_todays_appointments()
Service Model
text
Copy code
Properties:
- id, name, description, duration_minutes, price, category

Relationships:
- One Service → Many Appointments

Methods:
- create(), get_active(), find_by_category(), get_appointments()
Appointment Model
text
Copy code
Properties:
- id, client_id, stylist_id, service_id, appointment_date, status

Relationships:
- Belongs to Client, Stylist, and Service

Methods:
- create(), find_upcoming(), has_conflict(), cancel()
Technical Implementation
ORM Features
SQLAlchemy ORM

Four related tables with foreign keys

One-to-many relationships

Property methods for validation and formatting

Class methods for CRUD operations

CLI Features
Interactive menu navigation

Input validation

Clear error handling

Persistent SQLite storage

Business logic for scheduling and revenue calculations

Testing
Model Testing
bash
Copy code
python lib/test_models.py
Database Testing
bash
Copy code
python lib/debug.py
Seeding Data
bash
Copy code
python lib/seed.py
File Descriptions
lib/cli.py
Main CLI application responsible for:

Menu navigation

CRUD operations

Input validation

Reporting and search functionality

lib/models/
Contains SQLAlchemy ORM models:

client.py – Client data and appointment history

stylist.py – Stylist profiles and scheduling

service.py – Services with pricing and duration

appointment.py – Appointment scheduling and conflict detection

lib/database/init.py
Handles:

SQLite engine setup

Session management

Database initialization

lib/seed.py
Generates sample data using Faker

Useful for testing and demonstrations

lib/debug.py
Verifies database setup

Lists tables

Performs system checks

Project Requirements Met
ORM Requirements
Four model classes implemented

One-to-many relationships

Property methods for validation

CRUD operations for all models

CLI Requirements
Interactive menus

Application loop

CRUD functionality

Input validation

Clean object-oriented design

Additional Requirements
Proper project structure

Docstrings and documentation

Pipenv dependency management

Comprehensive README

Future Enhancements
Planned Features
Email appointment reminders

Online booking system

Inventory management

Employee time tracking

Mobile application

Technical Improvements
PostgreSQL support

Web interface using Flask or Django

REST API endpoints

CSV and Excel export

Automated database backups

Author
Benjakusa
Phase 3 Project – Flatiron School Software Engineering Program

License
This project is licensed under the MIT License. See the LICENSE file for details.