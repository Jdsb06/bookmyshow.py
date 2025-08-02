# 🎥 **BookMyShow - Python Console Application** 🛠️  
A simplified clone of **BookMyShow**, crafted in **Python** with **MySQL**, to manage users, shows, and bookings. Perfect for showcasing your skills in database-driven applications!  

---

## 👥 **Authors**

- **Jashandeep Singh**  
  [LinkedIn](https://www.linkedin.com/in/jdsb06) | [GitHub](https://github.com/Jdsb06)

- **Gravkrishna Gupta**  
  [LinkedIn](https://www.linkedin.com/in/garvkrishna-gupta-46639a325/) | [GitHub](https://github.com/Garvv06)


This project was developed as part of a **Class 12 Project** to demonstrate proficiency in Python and SQL.

---

## 💡 **Features**
- **User Management**: Sign-up, Sign-in, and account modification options.  
- **Show Management**: View trending shows and filter by genre (Movies, Comedy Shows, Concerts).  
- **Ticket Booking**: Simplified system for booking, viewing, and canceling tickets.  
- **Account Handling**: Modify user details or delete accounts securely.  

---

## 💾 **Database Overview**
The project connects to a **MySQL** database named `bookmyshow` with three main tables:  
1. **`user`**: Stores user data (ID, name, phone, password, city).  
2. **`shows`**: Maintains show details (ID, title, genre, available seats, rating, ticket price).  
3. **`booking`**: Records bookings (ID, user ID, show ID, number of tickets, total price).  

Sample data for the `shows` table is automatically added when you run the setup script.

---

## 📚 **Libraries Used**
- `pymysql` for database connection  
- `pandas` for data handling and report generation  

---

## 🚀 **How to Run**
1. Clone this repository:  
   ```bash
   git clone https://github.com/Jdsb06/bookmyshow.py.git
   cd bookmyshow.py
2. Run the setup script:
   ```bash
   python3 setup.py
