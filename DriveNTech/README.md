## Project Overview

**DriveNTech** is an intuitive and robust web application designed to help vehicle owners efficiently manage their vehicle maintenance and service schedules. Whether you want to keep track of service history, schedule upcoming repairs, or maintain vehicle records, DriveNTech streamlines the entire process with an easy-to-use interface.


## Features

- ✅ User Authentication (Register/Login/Logout)  
- ✅ Vehicle Management (Add, Update, Delete vehicles)  
- ✅ Service Scheduling with reminders  
- ✅ Maintain and view detailed Service History  
- ✅ Admin panel for easy backend management  


## Installation & Setup

Follow these steps to get DriveNTech up and running locally:

```bash
# Clone the repository
git clone https://github.com/se-thato/alx-project-nexus.git
cd alx-project-nexus/DriveNTech

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
