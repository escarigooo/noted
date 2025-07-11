# noted; - Digital Stationery Platform

## Project Overview

noted; is a Flask-based e-commerce platform for digital stationery products that I developed as my first significant programming project. This application demonstrates modern web development practices including modular architecture, blueprint-based routing, and service-oriented design patterns.

This is a learning project created to practice full-stack development skills, including:
- Building a Flask web application with proper architecture
- Implementing database models with SQLAlchemy
- Creating a complete e-commerce flow from browsing to checkout
- Developing an admin interface for product and order management

While this project is not in production use and some features may not be fully implemented, it represents my journey as a beginner developer tackling a complex application.

## Technical Requirements
- Python 3.8+
- MySQL 5.7+
- Modern web browser (Chrome, Firefox, Edge)
- WAMP/XAMPP for local development

## Getting Started

Follow these steps to set up and run the noted; application:

### 1. Setup the Environment

Run the setup script to create and configure the virtual environment:

```powershell
.\noted\setup_venv.bat
```

This script will:
- Create a Python virtual environment
- Install all required dependencies from requirements.txt
- Configure necessary environment settings

### 2. Start the Application

After setup is complete, start the Flask application:

```powershell
.\noted\start_project.bat
```

Alternatively, you can use the VS Code task:
1. Open the Command Palette (Ctrl+Shift+P)
2. Type "Tasks: Run Task"
3. Select "Start Flask App"

The application will be available at http://127.0.0.1:5000

### 3. Database Information

The application uses a MySQL database. Make sure you have MySQL installed and running.

- Default database name: `db_noted`
- Database script locations:
  - Main schema: `base-de-dados/db_noted.sql`
  - Test content: `base-de-dados/db_noted_conteudo-test.sql`

To initialize or reset the database, run:

```powershell
cd noted
python check_db.py
```

## Email Templates

The application includes several email templates for various user interactions:
- Registration and account verification
- Password reset
- Order confirmations
- Order status updates
- Invoices

All templates are located in `noted/templates/emails/`

## Project Architecture

### Directory Structure
The application follows a modular architecture:

```
noted/
├── __init__.py        # Flask application factory
├── app.py             # Application entry point
├── config.py          # Configuration management
├── models.py          # Database models (SQLAlchemy)
├── routes/            # Organized by feature using Flask Blueprints
│   ├── admin.py       # Admin dashboard functionality
│   ├── auth.py        # Authentication routes
│   ├── cart.py        # Shopping cart operations
│   ├── checkout.py    # Checkout process
│   ├── orders.py      # Order management
│   ├── products.py    # Product catalog
│   └── api/           # API endpoints
├── services/          # Business logic services
│   └── email_service.py  # Email functionality
├── static/            # Static assets (CSS, JS, images)
└── templates/         # Jinja2 templates
    ├── emails/        # Email templates
    ├── layout.html    # Base template
    ├── pages/         # Main page templates
    └── partials/      # Reusable components
```

### Frontend Organization
- **Base Template**: All pages extend `layout.html` with block content
- **Component Reuse**: Common elements (navbar, footer, product cards) are in `partials/`
- **CSS Organization**: Styles are organized by feature and component
- **JavaScript**: Feature-specific JS files with clear separation of concerns

### Backend Design
- **Blueprint Architecture**: Routes are organized in modular blueprints
- **Service Layer**: Business logic is separated into service classes
- **ORM**: SQLAlchemy models abstract database operations
- **Configuration**: Environment-based config with dotenv

## Key Features

### E-commerce Functionality
- Product catalog with categories and collections
- Shopping cart with session management
- Checkout process with order management
- User registration and account management

### Admin Interface
- Product and category management
- Order processing and status updates
- Customer management
- Basic sales analytics

### Security
- Password hashing with Werkzeug
- CSRF protection on all forms
- Secure session handling
- Email verification for new accounts

## Testing

To run the test suite:

```powershell
cd noted
python -m pytest
```

Key test files include:
- `test_email.py` - Email service functionality
- `test_cart_final.py` - Shopping cart operations
- `test_bulk_update.py` - Product updates
- `test_categories.py` - Category system

## API Endpoints

The application provides REST API endpoints for:

- `/api/products` - Product catalog access
- `/api/cart` - Cart management
- `/api/orders` - Order processing
- `/api/users` - User management (admin only)

## About the Developer

This project was independently developed by André Escarigo as a learning experience and portfolio project. As my first large-scale application, noted; represents my growth as a developer and my interest in creating well-structured web applications.

The project was built with a focus on applying modern development practices and design patterns I've learned through self-study. While not perfect, it demonstrates my approach to solving complex problems through modular design and separation of concerns.

## Future Development

As a learning project, noted; is continually evolving. Potential future enhancements include:
- Improved mobile responsiveness
- Integration with payment gateways
- Enhanced search functionality
- Performance optimizations
- Additional product categorization features

## License

This project is available under the MIT License.

Copyright (c) 2025 André Escarigo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

For questions or support, contact: escarigoandre@gmail.com

## Acknowledgements

This project was made possible thanks to the many excellent Flask and Python tutorials and documentation available to the community. Special thanks to:
- The Flask documentation team
- SQLAlchemy documentation
- The broader Python web development community