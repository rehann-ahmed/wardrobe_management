Wardrobe Management System

Wardrobe Management System is a web application designed to help users organize and manage their wardrobe efficiently. It allows users to register, log in, and manage outfits, get outfit suggestions, and plan their wardrobe using a calendar interface.

Features

User Registration and Login: Users can register with their username, password, and an optional profile picture.

Profile Picture Support: If no profile picture is uploaded during registration, a default profile image is used.

Dashboard: Provides an overview of the application features.

Manage Outfits: Add, view, and delete outfits with images and categories.

Outfit Suggestions: Randomized suggestions for outfits based on available wardrobe items.

Calendar Integration: Plan outfits for specific dates.

Sidebar Navigation: Collapsible sidebar with links to all major features.

Profile Dropdown: A dropdown menu with the user's profile picture, providing a logout option.

Tech Stack

Backend: Flask (Python)

Database: MySQL

Frontend: HTML, CSS, JavaScript

Hosting: Render for Flask app and Railway for MySQL database

Prerequisites

Python 3.11 or higher

MySQL server

Flask and Flask extensions

Installation

Step 1: Clone the Repository

git clone https://github.com/your-username/wardrobe-management.git
cd wardrobe-management

Step 2: Set Up Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Set Up the Database

Create a MySQL database named wardrobe_management.

Update the .env file with your database credentials:

MYSQL_DATABASE=wardrobe_management
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
SECRET_KEY=your_secret_key
UPLOAD_FOLDER=static/uploads

Initialize the database schema:

mysql -u root -p wardrobe_management < schema.sql

Step 5: Run the Application

flask run

The application will be accessible at http://127.0.0.1:5000.

Deployment

Backend Deployment

Use Render for hosting your Flask application.

Update the .env file with the database credentials provided by Render.

Database Deployment

Use Railway to host the MySQL database.

Copy the provided database credentials to your .env file.

Notes:

Ensure that the UPLOAD_FOLDER is correctly configured for your deployed environment.

File Structure

wardrobe-management/

├── app.py                 # Main Flask application

├── templates/             # HTML templates

├── static/

│   ├── css/               # CSS files

│   ├── js/                # JavaScript files

│   ├── uploads/           # User-uploaded profile pictures and outfit images

│   └── images/            # Default images (e.g., default profile picture)

├── schema.sql             # SQL script to initialize the database schema

├── requirements.txt       # Python dependencies

├── .env                   # Environment variables

└── README.md              # Project documentation

Screenshots

1. Dashboard



2. Manage Outfits



3. Outfit Suggestions



4. Calendar Integration



Contributing

Fork the repository.

Create a new branch for your feature: git checkout -b feature-name.

Commit your changes: git commit -m 'Add some feature'.

Push to the branch: git push origin feature-name.

Open a pull request.
