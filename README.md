# Recipe Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-blue.svg)](https://www.mysql.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A web application for managing and sharing recipes, built with Flask and MySQL.

## 📸 Screenshots

(Add screenshots here after deployment)

## ✨ Features

- **User Authentication**: Secure login and registration system
- **Recipe Management**: Create, read, update, and delete recipes
- **Category Organization**: Browse recipes by categories
- **Search Functionality**: Find recipes by title, description, or ingredients
- **Ingredient Database**: Manage ingredients with allergen information
- **Responsive Design**: Works on desktop and mobile devices
- **Image Upload**: Add images to your recipes

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Session-based authentication

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/recipe-management-system.git
cd recipe-management-system
```

### 2. Create a virtual environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Edit the `mysql_db.py` file and update the database configuration:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'recipe_management'
}
```

### 5. Initialize the database

```bash
python setup_mysql.py
```

### 6. Run the application

```bash
python mysql_app.py
```

### 7. Access the application

Open your web browser and navigate to: http://127.0.0.1:5000

## 👥 Default Users

The application is pre-configured with two sample users:

| Username | Password | Role |
|----------|----------|------|
| john_doe | password | Regular user with sample recipes |
| jane_smith | password | Regular user with sample recipes |

## 📁 Project Structure

```
recipe-management-system/
├── mysql_app.py         # Main application file
├── mysql_db.py          # Database access functions
├── forms.py             # Form definitions
├── setup_mysql.py       # Database setup script
├── fixed_schema.sql     # MySQL database schema
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css    # Custom CSS styles
│   └── uploads/         # Uploaded recipe images
└── templates/           # HTML templates
    ├── base.html        # Base template with layout
    ├── index.html       # Homepage
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── recipes.html     # Recipe listing
    ├── recipe_detail.html # Recipe details
    └── recipe_form.html # Recipe add/edit form
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Flask framework
- Bootstrap for the UI components
- MySQL database
- All open-source libraries used in this project 