from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import json
import os

app = Flask(__name__)
# Secret key for session security
app.secret_key = 'RC_Workspace_123_Secret'

class WorkspaceManager:
    def __init__(self, bookings_file, users_file):
        self.bookings_file = bookings_file
        self.users_file = users_file
        self.initialize_json_files()

    def initialize_json_files(self):
        if not os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_json_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def register_user(self, username, password):
        users = self.load_json_data(self.users_file)
        for user in users:
            if user['username'] == username:
                return False
        users.append({"username": username, "password": password})
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)
        return True

    def authenticate_user(self, username, password):
        users = self.load_json_data(self.users_file)
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def get_bookings(self):
        return self.load_json_data(self.bookings_file)

    def save_booking(self, name, room_type, date, time_slot):
        bookings = self.get_bookings()
        new_booking = {
            "id": datetime.now().strftime("%M%S"),
            "name": name,
            "room": room_type,
            "date": date,
            "time": time_slot,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        bookings.append(new_booking)
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, indent=4)

    def update_booking(self, booking_id, new_date, new_time):
        bookings = self.get_bookings()
        for b in bookings:
            if b['id'] == booking_id:
                b['date'] = new_date
                b['time'] = new_time
                break
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, indent=4)

    def delete_booking(self, booking_id):
        bookings = self.get_bookings()
        bookings = [b for b in bookings if b['id'] != booking_id]
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, indent=4)

manager = WorkspaceManager("bookings.json", "users.json")

# --- Central Validation Logic ---
def is_time_overlap(req_start, req_end, booked_time_str):
    try:
        book_start, book_end = booked_time_str.split(' - ')
        fmt = "%I:%M %p"
        rs = datetime.strptime(req_start, fmt)
        re = datetime.strptime(req_end, fmt)
        bs = datetime.strptime(book_start, fmt)
        be = datetime.strptime(book_end, fmt)
        
        if rs >= re:
            return True 
        return max(rs, bs) < min(re, be)
    except Exception:
        return True 

def is_past_time(req_date, req_start):
    try:
        fmt = "%Y-%m-%d %I:%M %p"
        req_dt = datetime.strptime(f"{req_date} {req_start}", fmt)
        return req_dt < datetime.now()
    except Exception:
        return True 

def validate_time_slot(room_name, date, start_time, end_time, current_booking_id=None):
    if is_past_time(date, start_time):
        return False, "Cannot set reservation to a past date/time."
    
    try:
        fmt = "%I:%M %p"
        rs = datetime.strptime(start_time, fmt)
        re = datetime.strptime(end_time, fmt)
        if rs >= re:
            return False, "End time must be strictly after the start time."
    except Exception:
        return False, "Invalid time format."

    bookings = manager.get_bookings()
    for b in bookings:
        if current_booking_id and b['id'] == current_booking_id:
            continue
            
        if b['room'] == room_name and b['date'] == date:
            if is_time_overlap(start_time, end_time, b['time']):
                return False, "The selected time slot is already booked."
                
    return True, ""


# --- Routes ---

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', is_logged_in=True, user_name=session['user'])
    else:
        return render_template('index.html', is_logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    action = request.form.get('action')
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return render_template('index.html', is_logged_in=False, error="Please fill in all fields.")

    if action == "signup":
        if manager.register_user(username, password):
            session['user'] = username 
            return redirect(url_for('home'))
        else:
            return render_template('index.html', is_logged_in=False, error="Username already exists.")
            
    elif action == "signin":
        if manager.authenticate_user(username, password):
            session['user'] = username 
            return redirect(url_for('home'))
        else:
            return render_template('index.html', is_logged_in=False, error="Invalid credentials.")

@app.route('/logout')
def logout():
    session.pop('user', None) 
    return redirect(url_for('home'))

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    all_rooms = [
        {"name": "CAIRO", "type": "Private"},
        {"name": "SANAA", "type": "Open Air"},
        {"name": "ASMARA", "type": "Coworker"},
        {"name": "KHARTOUM", "type": "Coworker"}
    ]

    if request.method == 'POST':
        search_date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        room_type_filter = request.form.get('room_type_filter')

        if not search_date or not start_time or not end_time:
            return render_template('rooms.html', error="Please select valid date and times.", search_active=False)

        is_valid, error_msg = validate_time_slot(None, search_date, start_time, end_time)
        if not is_valid and error_msg != "The selected time slot is already booked.":
            return render_template('rooms.html', error=error_msg, search_active=False)

        bookings = manager.get_bookings()
        available_rooms = []

        for room in all_rooms:
            if room_type_filter != "All" and room['type'] != room_type_filter:
                continue
                
            is_booked = False
            for b in bookings:
                if b['room'] == room['name'] and b['date'] == search_date:
                    if is_time_overlap(start_time, end_time, b['time']):
                        is_booked = True
                        break 
            
            if not is_booked:
                available_rooms.append(room)

        return render_template('rooms.html', rooms=available_rooms, search_active=True, s_date=search_date, s_start=start_time, s_end=end_time)

    return render_template('rooms.html', search_active=False)

@app.route('/book', methods=['POST'])
def book():
    if 'user' not in session:
        return redirect(url_for('home'))

    name = session['user']
    room_type = request.form.get('room_type')
    date = request.form.get('date')
    time_slot = request.form.get('time_slot')
    
    try:
        req_start, req_end = time_slot.split(' - ')
    except ValueError:
        return redirect(url_for('dashboard', error="Booking failed: Invalid time format."))

    is_valid, error_msg = validate_time_slot(room_type, date, req_start, req_end)
    
    if not is_valid:
        return redirect(url_for('dashboard', error=f"Booking failed: {error_msg}"))

    manager.save_booking(name, room_type, date, time_slot)
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))

    current_user = session['user']
    error_msg = request.args.get('error') 
    all_bookings = manager.get_bookings()
    
    user_bookings = [b for b in all_bookings if b['name'] == current_user]
        
    return render_template('dashboard.html', bookings=user_bookings, current_user=current_user, error=error_msg)

@app.route('/edit/<booking_id>', methods=['POST'])
def edit(booking_id):
    if 'user' not in session:
        return redirect(url_for('home'))
        
    new_date = request.form.get('new_date')
    new_start = request.form.get('new_start')
    new_end = request.form.get('new_end')
    
    bookings = manager.get_bookings()
    target_booking = None
    for b in bookings:
        if b['id'] == booking_id:
            target_booking = b
            break
            
    if not target_booking:
        return redirect(url_for('dashboard', error="Update failed: Booking record missing."))

    room_name = target_booking['room']

    is_valid, error_msg = validate_time_slot(room_name, new_date, new_start, new_end, current_booking_id=booking_id)
    
    if not is_valid:
        return redirect(url_for('dashboard', error=f"Update failed: {error_msg}"))
        
    new_time = f"{new_start} - {new_end}"
    manager.update_booking(booking_id, new_date, new_time)
    
    return redirect(url_for('dashboard'))

@app.route('/delete/<booking_id>', methods=['POST'])
def delete(booking_id):
    if 'user' not in session:
        return redirect(url_for('home'))

    manager.delete_booking(booking_id)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)