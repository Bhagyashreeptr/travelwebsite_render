from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import webbrowser
import re  # for validation

# --- Create Flask app ---
app = Flask(__name__)
app.secret_key = "supersecretkey123"  # required for flash messages

# --- MySQL Connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",                # your MySQL user
    password="bhagyashree@123", # your exact password
    database="travel_db"
)
cursor = db.cursor(dictionary=True)

# --- Home Page ---
@app.route('/')
def home():
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()
    return render_template('home.html', flights=flights, hotels=hotels)

# --- Booking Page ---
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        country_code = request.form.get('country_code')
        phone = request.form['phone']
        full_phone = f"{country_code}{phone}"
        flight_id = request.form['flight']
        hotel_id = request.form['hotel']

        # --- Validation ---
        if not re.match("^[A-Za-z ]+$", name):
            return "❌ Error: Name must contain only alphabets."

        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            return "❌ Error: Email must be a valid Gmail address."

        if not re.match(r"^[0-9]{10}$", phone):
            return "❌ Error: Phone must be exactly 10 digits."

        if not flight_id or not hotel_id:
            return "❌ Error: Please select both flight and hotel."

        # Insert customer info
        cursor.execute(
            "INSERT INTO customers (name,email,phone) VALUES (%s,%s,%s)",
            (name, email, full_phone)
        )
        db.commit()
        customer_id = cursor.lastrowid

        # Insert booking info
        cursor.execute(
            "INSERT INTO bookings (customer_id, flight_id, hotel_id, status) VALUES (%s,%s,%s,'Booked')",
            (customer_id, flight_id, hotel_id)
        )
        db.commit()

        return render_template('success.html')

    # GET request: show booking form
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()
    return render_template('booking.html', flights=flights, hotels=hotels)

# --- Reports Page ---
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        if booking_id:
            upd_cursor = db.cursor()
            # Delete the booking
            upd_cursor.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
            db.commit()
            upd_cursor.close()
            flash("Flight cancellation was successful ✅", "success")
        return redirect(url_for('reports'))

    cursor.execute(
        "SELECT b.id, c.name AS customer_name, c.email, c.phone, "
        "f.name AS flight_name, f.source, f.destination, "
        "h.name AS hotel_name, b.status "
        "FROM bookings b "
        "JOIN customers c ON b.customer_id = c.id "
        "JOIN flights f ON b.flight_id = f.id "
        "JOIN hotels h ON b.hotel_id = h.id "
        "WHERE b.status = 'Booked' "
        "ORDER BY b.id DESC"
    )
    report_data = cursor.fetchall()
    return render_template('reports.html', report_data=report_data)

# --- Run Flask and auto-open browser ---
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
