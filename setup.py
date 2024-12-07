"""
====================================================
IMPORTANT NOTES:
1. This project is designed for Unix-based systems (Linux/macOS).
2. Use Python 3 to run the script. Ensure you have `python3` installed.
3. MySQL must be installed and running locally on your system.
4. During setup, you will be prompted to enter your MySQL root password.
5. The `setup.py` script will:
   - Install required Python libraries.
   - Create the `bookmyshow` database and tables.
   - Populate tables with sample data.
   - Update `main.py` with your MySQL root password.
   - Run the application.
6. If you encounter issues with the `python` command, use `python3` instead or create an alias:
   alias python=python3
====================================================
"""


import subprocess
import pymysql

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

def setup_database(mysql_password):
    print("Setting up the database...")
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password=mysql_password
    )
    cursor = conn.cursor()

    with open("db_setup.sql", "r") as f:
        sql_commands = f.read()

    for command in sql_commands.split(";"):
        if command.strip():
            cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete.")

def update_main_password(mysql_password):
    print("Updating the MySQL password in main.py...")
    with open("main.py", "r") as file:
        main_content = file.read()

    # Replace the placeholder PASSWORD with the actual password
    updated_content = main_content.replace("password=\"\"", f"password=\"{mysql_password}\"")

    with open("main.py", "w") as file:
        file.write(updated_content)
    print("main.py updated successfully.")

def run_project():
    print("Running the project...")
    subprocess.run(["python3", "main.py"])

if __name__ == "__main__":
    install_dependencies()

    # Prompt the user for MySQL password
    mysql_password = input("Enter your MySQL root password: ").strip()

    setup_database(mysql_password)
    update_main_password(mysql_password)
    run_project()
