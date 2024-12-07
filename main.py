"""
====================================================
IMPORTANT NOTES:
1. This script is automatically updated by `setup.py` 
   with the MySQL root password during the setup process.
2. Ensure you run `setup.py` before running `main.py`.
3. This project assumes the `bookmyshow` database has
   been set up with the correct tables and sample data.
4. If you make changes to the database schema, update 
   the `db_setup.sql` file accordingly and re-run `setup.py`.
====================================================
"""


import pymysql
import os
import pandas as pd
import platform

conn = pymysql.connect(host="localhost",
                               user="root",
                               password="",                                        #add your password
                               database="bookmyshow")
cursor = conn.cursor()

current_user_id, ch, opp, opt = None, None, None, None
user_id = None


def signup():
    global current_user_id, user_id
    l = []
    try:
        print("Please enter integer value only.")
        user_id = int(input("Enter User ID: "))
        l.append(user_id)
    except ValueError:
        print("Invalid input for username. Please enter a valid integer.")
        signup()
    user_name = input("Enter your name: ")
    l.append(user_name)

    try:
        phone = int(input("Enter your Phone number: "))
        l.append(phone)
    except ValueError:
        print("Invalid input for phone number. Please enter a valid integer.")
        print("Please Try again")
        return signup()

    pass_word = input("Enter your password: ")
    l.append(pass_word)
    city = input("Enter your city: ")
    l.append(city)

    cust = tuple(l)
    try:
        sql = "INSERT INTO user (user_id, user_name, Phone, pass_word, city) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, cust)
        conn.commit()
        print("Welcome to Bookmyshow")
        current_user_id = user_id
        menu_set()
    except mysql.connector.Error as err:
        print(f"Error during sign-up: {err}")
        print("Please Try again")
        menu()
    else:
        print("Invalid Input .PLease enter a valid input")


def signin():
    global current_user_id, user_id
    try:
        user_id = int(input("Enter your User ID: "))
    except ValueError:
        print("Invalid input for username. Please enter a valid integer.")
        signin()
    pass_word = input("Enter Your Password: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id = %s AND pass_word = %s", (user_id, pass_word))
    user = cursor.fetchone()
    if user:
        current_user_id = user_id
        print("Sign-in successful!")
        menu_set()
    else:
        print()
        print("Invalid credentials.")
        print("Try Again")
        menu()


def menu_set():
    global current_user_id
    global opt
    print()
    print("======================================================")
    print("             WELCOME TO BOOKMYSHOW                    ")
    print("======================================================")
    print("1. Book Shows")
    print("2. View Your booking")
    print("3. Cancel your booking ")
    print("4. View/Modify you account")
    print("5. Trending Shows")
    print("6. Sign Out")
    try:
        opt = input(" Enter your choice: ")
    except:
        print("Invalid Input .Please Enter a valid input")
        menu_set()

    if opt == '1':
        booking_shows()
        run_again()
    elif opt == '2':
        display_user_bookings(user_id)
        run_again()
    elif opt == '3':
        cancel_booking(cursor, current_user_id)
        run_again()
    elif opt == '4':
        modify_view_account()
        run_again()
    elif opt == '5':
        view_trending_shows()
        run_again()
    elif opt == '6':
        print("Signing Out....")
        menu()
        run_again()
    else:
        print("Invalid Input")
        menu_set()


def booking_shows():
    def book_tickets():
        """Book tickets for an event (movie, comedy show, or concert) and display payment information using pandas DataFrame."""
        while True:  # Add a loop to allow multiple bookings
            user_id = current_user_id

            print("Choose the event type You Want To Book: ")
            print("1. Movie")
            print("2. Comedy Show")
            print("3. Concert")

            while True:
                event_choice = input("Enter the number for the event type you want to book (1/2/3): ")
                if event_choice not in ['1', '2', '3']:
                    print("Invalid choice. Please enter a valid number (1/2/3).")
                else:
                    break

            event_type = {
                '1': 'movie',
                '2': 'comedy show',
                '3': 'concert'
            }[event_choice]

            if event_type == 'movie':
                table_name = "shows where genre ='movie'"
            elif event_type == 'comedy show':
                table_name = "shows where genre ='comedy shows'"
            elif event_type == 'concert':
                table_name = "shows where genre ='concert'"
            else:
                print("Invalid event type.")
                continue  # Restart the loop if the event type is invalid

            while True:
                display_data(table_name)  # Display available events

                show_id = input(f"Enter the {event_type} show ID you want to book: ")
                if not show_id.strip():
                    print("Show ID cannot be blank.")
                    continue

                # Check if the entered show ID is valid for the selected event type
                if not valid_id(show_id, event_type):
                    print(f"Invalid {event_type} show ID. Please enter a valid one.")
                    continue

                break

            while True:
                num_tickets = input("Enter the number of tickets: ")
                if not num_tickets.strip():
                    print("Invalid number of tickets. Please enter a valid number greater than 0.")
                elif not num_tickets.isdigit() or int(num_tickets) < 0:
                    print("Invalid number of tickets. Please enter a valid number greater than or equal to 0.")
                else:
                    num_tickets = int(num_tickets)
                    if num_tickets == 0:
                        print("Invalid number of tickets. Please enter a valid number greater than 0.")
                    else:
                        break

            book_tickets_with_user_info(cursor, user_id, show_id, event_type, num_tickets)

            # Ask if the user wants to book another event
            conf = input("Do you want to book another event? (Y/N): ")
            if conf.lower() != "y":
                break  # Exit the loop if the user doesn't want to book another event

    def valid_id(show_id, event_type):
        """Check if the entered show ID is valid for the specified event type."""
        if event_type == 'movie':
            table_name = "shows where genre = 'movie'"
        elif event_type == 'comedy show':
            table_name = "shows where genre = 'comedy shows'"
        elif event_type == 'concert':
            table_name = "shows where genre = 'concert'"
        else:
            print("Invalid event type.")
            return False

        query = f"SELECT COUNT(*) FROM {table_name} AND show_id = %s"
        cursor.execute(query, (show_id,))
        count = cursor.fetchone()[0]
        return count > 0

    def display_data(table_name):
        """Display available events (movies, comedy shows, or concerts) from the database using pandas DataFrame."""
        cursor.execute(f"SELECT * FROM {table_name}")
        events_data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        events_df = pd.DataFrame(events_data, columns=columns)
        print(f"\nAvailable {table_name.replace('_', ' ').title()}:")
        print(events_df)

    def book_tickets_with_user_info(cursor, user_id, event_id, event_type, num_tickets):
        """Book tickets for an event (movie, comedy show, or concert) with user info and display payment information using pandas DataFrame."""

        table_name = "shows" if event_type == "movie" else "shows" if event_type == "comedy show" else "shows"
        cursor.execute(f"SELECT title, available_seats FROM {table_name} WHERE show_id = %s", (event_id,))
        event_data = cursor.fetchone()

        if event_data is None:
            print(f"Invalid {event_type} ID.")
            return

        event_title, available_seats = event_data

        if available_seats < num_tickets:
            print(f"Sorry, there are only {available_seats} seats available for {event_title}.")
            return

        total_price = calculate_ticket_price(event_id, event_type, num_tickets)

        # Simulated payment processing (replace with real payment gateway)
        payment_successful = simulate_payment(total_price)

        if payment_successful:
            cursor.execute(
                "INSERT INTO booking (user_id, user_name, show_id, num_tickets) VALUES (%s, %s, %s, %s)",
                (user_id, get_user_name(user_id), event_id, num_tickets))
            cursor.execute(f"UPDATE {table_name} SET available_seats = available_seats - %s WHERE show_id = %s",
                           (num_tickets, event_id))


            # Retrieve the generated booking ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            booking_id = cursor.fetchone()[0]

            # Update the booking record with the generated booking ID and total price
            cursor.execute("UPDATE booking SET booking_id = %s, Total_price = %s WHERE user_id = %s AND show_id = %s",
                           (booking_id, total_price, user_id, event_id))
            conn.commit()

            # Display payment information
            payment_data = {'User ID': [user_id], 'User Name': [get_user_name(user_id)],
                            'Event Type': [event_type.title()],
                            'Event Title': [event_title], 'Total Price': [total_price], 'Booking ID': [booking_id]}
            payment_df = pd.DataFrame(payment_data)
            print("\nPayment Details:")
            print(payment_df)

            # Ask for confirmation
            confr = input("Are you sure you want to confirm this booking? (Y/N): ")
            if confr.lower() == "y":
                print("Booking confirmed.")
            else:
                # Handle cancellation if the user doesn't confirm
                print("Booking canceled.")
        else:
            # Handle payment failure
            print("Payment was not successful. Booking canceled.")

    def calculate_ticket_price(event_id, event_type, num_tickets):
        # Define a query to retrieve the ticket price from the shows table
        query = f"SELECT ticket_price FROM shows WHERE show_id = '{event_id}'"

        # Execute the query to fetch the ticket price
        cursor.execute(query)
        price_data = cursor.fetchone()

        if price_data:
            price_per_ticket = price_data[0]
        else:
            # Default price if event_id is not found
            price_per_ticket = 200  # You can set a default price here

        # Calculate the total price
        total_price = price_per_ticket * num_tickets
        return total_price

    def simulate_payment(total_price):
        # Simulate successful payment (replace with real payment processing)
        return True

    def get_user_name(user_id):
        """Retrieve user name from the users table using user ID."""
        cursor.execute("SELECT user_name FROM user WHERE user_id = %s", (user_id,))
        user_name = cursor.fetchone()
        if user_name:
            return user_name[0]
        else:
            return "Unknown User"

    book_tickets()  # Call your booking function

def display_user_bookings(user_id):
    """Display the bookings of the signed-in user and save them to a CSV file."""
    cursor.execute("SELECT booking_id, show_id, num_tickets, total_price FROM booking WHERE user_id = %s",
                   (user_id,))
    user_bookings = cursor.fetchall()

    if not user_bookings:
        print("You don't have any bookings.")
        input("Press Enter to return to the main menu...")
        return

    # Display user's bookings
    print("\nYour Bookings:")
    for booking in user_bookings:
        booking_id, show_id, num_tickets, total_price = booking

        # Retrieve the event title
        cursor.execute("SELECT title FROM shows WHERE show_id = %s", (show_id,))
        event_data = cursor.fetchone()
        if event_data:
            event_title = event_data[0]
        else:
            event_title = "Unknown Event"

        print(f"Booking ID: {booking_id}")
        print(f"Event Title: {event_title}")
        print(f"Number of Tickets: {num_tickets}")
        print(f"Total Price: ₹{total_price}")
        print()

    df = pd.DataFrame(user_bookings,
                      columns=["Booking ID", "Show ID", "Number of Tickets", "Total Price"])

    event_titles = []
    for show_id in df["Show ID"]:
        cursor.execute("SELECT title FROM shows WHERE show_id = %s", (show_id,))
        event_data = cursor.fetchone()
        event_title = event_data[0] if event_data else "Unknown Event"
        event_titles.append(event_title)

    df["Event Title"] = event_titles

    csv_filename = f"user_{user_id}_bookings.csv"

    # Append new bookings to the existing CSV file or create a new file with headers
    if not pd.DataFrame(columns=df.columns).empty:
        df.to_csv(csv_filename, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_filename, index=False)

    print(f"Your bookings have been saved to '{csv_filename}'.")

    input("Press Enter to return to the main menu...")
def cancel_booking(cursor, user_id):
    while True:
        cursor.execute("SELECT booking_id, show_id, num_tickets, total_price FROM booking WHERE user_id = %s", (user_id,))
        user_bookings = cursor.fetchall()

        if not user_bookings:
            print("You don't have any bookings to cancel.")
            return

        print("Your Bookings:")
        for booking in user_bookings:
            booking_id, show_id, num_tickets, total_price = booking

            # Retrieve the event title
            cursor.execute("SELECT title FROM shows WHERE show_id = %s", (show_id,))
            event_data = cursor.fetchone()
            if event_data:
                event_title = event_data[0]
            else:
                event_title = "Unknown Event"

            print(f"Booking ID: {booking_id}")
            print(f"Event Title: {event_title}")
            print(f"Number of Tickets: {num_tickets}")
            print(f"Total Price: ₹{total_price}")
            print()

        booking_id_to_cancel = input("Enter the Booking ID to cancel (or '0' to cancel nothing): ").strip()

        if booking_id_to_cancel == '0':
            print("Booking cancellation canceled.")
            return

        password_confirmation = input("Please enter your password to confirm the cancellation: ").strip()

        cursor.execute("SELECT pass_word FROM user WHERE user_id = %s", (user_id,))
        user_password = cursor.fetchone()

        if user_password:
            user_password = user_password[0]

            if password_confirmation == user_password:
                cursor.execute("SELECT * FROM booking WHERE booking_id = %s AND user_id = %s", (booking_id_to_cancel, user_id))
                booking_data = cursor.fetchone()

                if booking_data:
                    user_id, show_id, num_tickets, total_price = booking_data[1], booking_data[3], booking_data[4], booking_data[5]

                    # Retrieve the event title
                    cursor.execute("SELECT title FROM shows WHERE show_id = %s", (show_id,))
                    event_data = cursor.fetchone()
                    if event_data:
                        event_title = event_data[0]
                    else:
                        event_title = "Unknown Event"

                    confirm = input(f"Do you want to cancel Booking ID {booking_id_to_cancel} for {event_title}? (Y/N): ").strip().lower()

                    if confirm == 'y':
                        cursor.execute("DELETE FROM booking WHERE booking_id = %s", (booking_id_to_cancel,))
                        cursor.execute("UPDATE shows SET available_seats = available_seats + %s WHERE show_id = %s",
                                       (num_tickets, show_id))
                        conn.commit()

                        print(f"Booking {event_title} with Booking ID {booking_id_to_cancel} has been canceled.")
                        print(f" ₹{total_price} Refund will be initiated soon.")
                    else:
                        print("Booking cancellation canceled.")
                else:
                    print("Booking not found")
            else:
                print("Password confirmation failed.")
                choice = input("Do you want to try again? (Y/N): ").strip().lower()
                if choice != 'y':
                    print("Returning to the main menu.")
                    return

        another_cancel = input("Do you want to cancel another booking? (Y/N): ").strip().lower()
        if another_cancel != 'y':
            print("Returning to the main menu.")
            return


def modify_view_account():
    conn = pymysql.connect(host="localhost",
                                   user="root",
                                   password="",                                                  #ADD YOUR PASSWORD
                                   database="bookmyshow")
    global current_user_id
    global ch, opp
    print()
    print("What do you want to do")
    print("1. View Account")
    print("2. Modify Account")
    print("3. Delete Your Account")
    try:
        ch = int(input("Enter your choice: "))
    except:
        print("Invalid input .Please Enter a valid Input")
    if ch == 1:
        print()
        query = "SELECT user_name,phone,city from user where user_id = %s"
        cursor = conn.cursor()
        values = (current_user_id,)
        cursor.execute(query, values)
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=['Name', 'Phone Number', 'City'])
        print(df)
    elif ch == 2:
        print("What do you want to change?: ")
        print("1. Name")
        print("2. Phone Number")
        print("3. Password")
        print("4. City")
        try:
            opp = int(input("Enter your choice: "))
        except:
            print("Invalid Input")
        if opp == 1:
            new_name = input("Enter your Name: ")
            query = "update user set user_name = " + "'" + new_name + "'" + "where user_id=" + str(user_id)
            cursor_ = conn.cursor()
            cursor_.execute(query)
            conn.commit()
            print("Your name has been updated")
        elif opp == 2:
            new_phone = input("Enter Phone Number: ")
            query = "update user set phone = " + "'" + new_phone + "'" + "where user_id=" + str(user_id)
            cursor_ = conn.cursor()
            cursor_.execute(query)
            conn.commit()
            print("Your Phone number has been updated")
        elif opp == 3:
            old_pass = input("Enter your old password: ")
            query = "SELECT pass_word from user where user_id = %s"
            cursor = conn.cursor()
            values = (user_id,)
            cursor.execute(query, values)
            res = cursor.fetchall()
            df = pd.DataFrame(res, columns=['password'])
            result_string = df['password'].str.strip()[0]
            if result_string == old_pass:
                new_pass = input("Enter new password: ")
                query = "update user set pass_word = " + "'" + new_pass + "'" + "where user_id=" + str(user_id)
                cursor_ = conn.cursor()
                cursor_.execute(query)
                conn.commit()
                print("Your password has been updated")
            else:
                print("You entered wrong password")
                print("Please Try again")

        elif opp == 4:
            new_city = input("Enter new city")
            query = "update user set city = " + "'" + new_city + "'" + "where user_id=" + str(user_id)
            cursor_ = conn.cursor()
            cursor_.execute(query)
            conn.commit()
            print("Your city has been updated")
        else:
            print("Wrong Operation ")
    elif ch == 3:
        try:
            confirm = input("Are you sure you want to delete your account? (y/n): ").strip().lower()
            if confirm == 'y':
                old_pass = input("Enter your password: ")
                query = "SELECT pass_word from user where user_id = %s"
                cursor = conn.cursor()
                values = (current_user_id,)
                cursor.execute(query, values)
                res = cursor.fetchall()
                result_string = res[0][0]
                if result_string == old_pass:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
                    conn.commit()
                    print("Your account has been deleted.")
                    menu()
                else:
                    print("You entered wrong password")
            else:
                print("Account deletion canceled.")
        except mysql.connector.Error as err:
            print(f"Error during account deletion: {err}")

    else:
        print("Wrong operation")


def view_trending_shows():
    query = "SELECT Title as Shows, Genre ,Rating FROM shows WHERE Rating >= 9.0;"
    cursor.execute(query)
    res = cursor.fetchall()
    print("Trending Shows:")
    df = pd.DataFrame(res, columns=['Shows', 'Genre', 'Rating'])
    print(df.squeeze())


def run_again():
    choice = input("Do you want to continue:y/n : ").strip().lower()
    if choice == 'y':
        if platform.system() == "Windows":
            print(os.system('cls'))
        menu_set()

    elif choice == 'n':
        print("What do you want to do :-")
        print("1. Return to main menu")
        print("2. Sign out")
        print("3. Exit")
        try:
            enter = input("Enter your choice: ").strip().lower()
            if enter == '1':
                menu_set()
            elif enter == '2':
                print("Signing Out...")
                menu()
            elif enter == '3':
                exit()
            else:
                print("Invalid input")
        except ValueError:
            print("Please enter a valid Input")
            run_again()
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        return run_again()


def menu():
    print("1. Sign up")
    print("2. Sign in")
    print("3. Exit")
    try:
        choice = input("Enter your choice: ")
        if choice == '1':
            signup()
        elif choice == '2':
            signin()
        elif choice == '3':
            exit()
        else:
            print("Invalid choice. Please choose again.")
            print()
            menu()
    except mysql.connector.Error as err:
        print(f"Error during sign-up: {err}")


menu()
print("Thanks for using BookMyShow")
