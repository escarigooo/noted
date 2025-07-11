# noted; - Digital Stationery Platform

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

## Contact

For questions or support, contact: escarigoandre@gmail.com