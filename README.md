# AegisCore

AegisCore is a Django-based web application designed for administrative, user, and guest management with modular apps for Admin, Basics, Guest, and User functionalities. It features user registration, authentication, admin dashboards, category and place management, and more. The project is structured for scalability and maintainability, making it suitable for educational, demo, or production use with further customization.

## Features
- Modular Django apps: Admin, Basics, Guest, User
- User registration and authentication
- Admin dashboard with category, district, and place management
- SIEM (Security Information and Event Management) dashboard and alerts
- Basic utilities (calculator, data operations)
- Static and media file management
- Template-based UI for each module

## Project Structure
```
AegisCore/           # Django project settings and core configuration
Admin/               # Admin app: models, views, templates, migrations
Basics/              # Basics app: models, views, templates, migrations
Guest/               # Guest app: models, views, templates, migrations, static files
User/                # User app: models, views, templates, migrations
Assets/              # User-uploaded files (e.g., photos)
db.sqlite3           # SQLite database file
manage.py            # Django management script
req.txt              # Python dependencies
```

### Key Folders and Files
- **AegisCore/**: Django project settings (settings.py, urls.py, wsgi.py, asgi.py)
- **Admin/**: Admin-specific logic, templates (AdminRegistration, Category, District, etc.)
- **Basics/**: Basic utilities and templates (Calculator, Data, Largest, etc.)
- **Guest/**: Guest-facing pages, static assets, and templates (Login, Userregistration, etc.)
- **User/**: User profile management, templates (EditProfile, Homepage, etc.)
- **Assets/**: User-uploaded media (e.g., profile photos)
- **db.sqlite3**: Default SQLite database
- **manage.py**: Django's command-line utility
- **req.txt**: List of required Python packages

## Installation Steps

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- (Optional) Virtual environment tool (venv, virtualenv)

### Setup Instructions
1. **Clone the repository**
   ```sh
   git clone <repository-url>
   cd AegisCore
   ```

2. **Create and activate a virtual environment (recommended)**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r req.txt
   ```

4. **Apply database migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to: http://127.0.0.1:8000/

## Usage
- Admin, User, and Guest modules are accessible via their respective URLs and templates.
- Static files and templates are organized by app for easy customization.
- Use the Django admin panel for backend management.

## Contributing
Feel free to fork the repository, create issues, or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact the project maintainer.
