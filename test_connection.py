import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="bhagyashree@123",
        database="travel_db"
    )
    print("Connected to MySQL from Flask!")
except mysql.connector.Error as err:
    print("Error:", err)
