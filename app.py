from flask import Flask, render_template, request, redirect, url_for, flash
import webbrowser

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# --- Dummy Data ---
flights = [
    {"id": 1, "name": "Air India", "source": "Delhi", "destination": "Mumbai"},
    {"id": 2, "name": "IndiGo", "source": "Bangalore", "destination": "Chennai"},
]

hotels = [
    {"id": 1, "name": "Taj Hotel", "location": "Mumbai"},
    {"id": 2, "name": "ITC Gardenia", "location": "Bangalore"},
]

bookings = []  # store bookings in memory (clears if server restarts)

# --- Home Page ---
@app.route('/')
def home():
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

        # Save booking
        booking = {
            "id": len(bookings) + 1,
            "customer_name": name,
            "email": email,
            "phone": full_phone,
            "flight": next(f for f in flights if str(f["id"]) == flight_id),
            "hotel": next(h for h in hotels if str(h["id"]) == hotel_id),
            "status": "Booked"
        }
        bookings.append(booking)
        return render_template('success.html')

    return render_template('booking.html', flights=flights, hotels=hotels)

# --- Reports Page ---
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        booking_id = int(request.form.get('booking_id'))
        for b in bookings:
            if b["id"] == booking_id:
                b["status"] = "Cancelled"
        flash("Flight cancellation was successful ✅", "success")
        return redirect(url_for('reports'))

    return render_template('reports.html', report_data=bookings)

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
