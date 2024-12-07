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
    subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    install_dependencies()

    # Prompt the user for MySQL password
    mysql_password = input("Enter your MySQL root password: ").strip()

    setup_database(mysql_password)
    update_main_password(mysql_password)
    run_project()
