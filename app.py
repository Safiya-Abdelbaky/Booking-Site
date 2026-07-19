from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

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


# SignUp function
    def register_user(self, username, password):
        users = self.load_json_data(self.users_file)
        for user in users:
            # must be uniqe as it's his ID
            if user['username'] == username:
                return False
        users.append({"username": username, "password": password})
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)
        return True

#SignIn function
    def authenticate_user(self, username, password):
        users = self.load_json_data(self.users_file)
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def save_booking(self, name, room_type, date, time_slot):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        booking_id = datetime.now().strftime("%M%S")
        bookings = self.load_json_data(self.bookings_file)
        
        new_booking = {
            "id": booking_id,
            "name": name,
            "room": room_type,
            "date": date,
            "time": time_slot,
            "created_at": timestamp
        }
        bookings.append(new_booking)
        
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, indent=4)

    # Wrapper Function or shortcut        
    def get_bookings(self):
        return self.load_json_data(self.bookings_file)

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
        # add all data except the id you want to delete and write them in the file
        bookings = [b for b in bookings if b['id'] != booking_id]
        with open(self.bookings_file, 'w', encoding='utf-8') as f:
            json.dump(bookings, f, indent=4)

    def load_json_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

manager = WorkspaceManager("bookings.json", "users.json")

# --- Time Validation Algorithms ---
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
        req_datetime_str = f"{req_date} {req_start}"
        req_dt = datetime.strptime(req_datetime_str, fmt)
        return req_dt < datetime.now()
    except Exception:
        return True 

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    action = request.form.get('action') 
    
    if not username or not password:
        return render_template('index.html', error="Please fill in all fields.")

    if action == "signup":
        if manager.register_user(username, password):
            return render_template('index.html', success_login=True, user_name=username)
        else:
            return render_template('index.html', error="Username already exists. Try signing in.")
            
    elif action == "signin":
        if manager.authenticate_user(username, password):
            return render_template('index.html', success_login=True, user_name=username)
        else:
            return render_template('index.html', error="Invalid credentials. Access Denied.")

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    all_rooms = [
        {"name": "CAIRO Room", "type": "Private"},
        {"name": "SANAA Space", "type": "Open Air"},
        {"name": "ASMARA Hub", "type": "Coworker"},
        {"name": "KHARTOUM Desk", "type": "Coworker"}
    ]

    if request.method == 'POST':
        search_date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        room_type_filter = request.form.get('room_type_filter')

        if not search_date or not start_time or not end_time:
            return render_template('rooms.html', error="Please select valid date and times.", search_active=False)

        # Server-side check: Prevent searching for past times
        if is_past_time(search_date, start_time):
            return render_template('rooms.html', error="Cannot book a time slot in the past. Please select a future time.", search_active=False)

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

        return render_template('rooms.html', 
                               rooms=available_rooms, 
                               search_active=True,
                               s_date=search_date,
                               s_start=start_time,
                               s_end=end_time)

    return render_template('rooms.html', search_active=False)

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('client_name')
    room_type = request.form.get('room_type')
    date = request.form.get('date')
    time_slot = request.form.get('time_slot')
    
    manager.save_booking(name, room_type, date, time_slot)
    return redirect(url_for('dashboard', user=name))

@app.route('/dashboard')
def dashboard():
    current_user = request.args.get('user')
    error_msg = request.args.get('error') 
    all_bookings = manager.get_bookings()
    
    if current_user:
        user_bookings = [b for b in all_bookings if b['name'] == current_user]
    else:
        user_bookings = []
        
    return render_template('dashboard.html', bookings=user_bookings, current_user=current_user, error=error_msg)

@app.route('/edit/<booking_id>', methods=['POST'])
def edit(booking_id):
    new_date = request.form.get('new_date')
    new_start = request.form.get('new_start')
    new_end = request.form.get('new_end')
    current_user = request.form.get('current_user')
    
    # Check if the updated time is in the past
    if is_past_time(new_date, new_start):
        return redirect(url_for('dashboard', user=current_user, error="Update failed: Cannot set reservation to a past date/time."))
    
    bookings = manager.get_bookings()
    target_booking = None
    for b in bookings:
        if b['id'] == booking_id:
            target_booking = b
            break
            
    if not target_booking:
        return redirect(url_for('dashboard', user=current_user, error="Booking record missing."))

    room_name = target_booking['room']
    
    has_overlap = False
    for b in bookings:
        if b['id'] != booking_id and b['room'] == room_name and b['date'] == new_date:
            if is_time_overlap(new_start, new_end, b['time']):
                has_overlap = True
                break
    
    if has_overlap:
        return redirect(url_for('dashboard', user=current_user, error="Update failed: The selected time slot is already booked by someone else."))
        
    new_time = f"{new_start} - {new_end}"
    manager.update_booking(booking_id, new_date, new_time)
    
    return redirect(url_for('dashboard', user=current_user))

@app.route('/delete/<booking_id>', methods=['POST'])
def delete(booking_id):
    current_user = request.form.get('current_user')
    manager.delete_booking(booking_id)
    return redirect(url_for('dashboard', user=current_user))

if __name__ == '__main__':
    app.run(debug=True)