from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

#Class Definition
class workspace:
    #The Constructor
    def __init__(self,bookings_file,users_file):
        self.bookings_file= bookings_file
        self.users_file = users_file
        self._initialize_files()



    def _initialize_files(self):
        for file_path in [self.bookings_file, self.users_file]:
            if not os.path.exists(file_path):
                with open(file_path,'w') as f:
                    json.dump([],f)

    def _read_data(self,filepath):
        try:
            with open(filepath,'r') as f:
                return json.load(f)
        except Exception:
            return[]

    def _write_data(self,filepath,data):
        with open(filepath,'w') as f:
            json.dump(data,f)

    def register_user(self,username,password):
        users = self._read_data(self.users_file)

        for user in users:
            if user['username'] == username:
                return False
            
        users.append({"username":username,"password":password})
        self._write_data(self.users_file,users)
        return True

    def authenticate_user(self,username,password):
        users = self._read_data(self.users_file)
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False
    
    
manager=workspace("bookings.json","users.json")

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

@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    action = request.form.get('action')

    if not username or not password:
        return render_template('index.html',error="Please fill in all fields")
    if action == "signup":
        if manager.register_user(username,password):
            return render_template('index.html',success_login=True,user_name=username)
        else:
            return render_template('index.html',error="Username already exists")

    elif action == "signin":
        if manager.authenticate_user(username,password):
            return render_template('index.html',success_login=True,user_name=username)
        else:
            return render_template('index.html',error="Invalid credentials") 


@app.route('/rooms',methods=['GET', 'POST'])
def rooms():
    all_rooms = [
        {"name": "CAIRO ", "type": "Private"},
        {"name": "SANAA ", "type": "Open Air"},
        {"name": "ASMARA ", "type": "Coworker"},
        {"name": "KHARTOUM ", "type": "Coworker"}
        ]
    if request.method == 'POST':
        search_date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('room_type_filter')
        room_type_filter = request.form.get('room_type_filter')

        if not search_date or not start_time or not end_time:
            return render_template('rooms.html', error="Please select valid date and times", search_active=False) 
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
        


if __name__ == '__main__':
    app.run(debug=True)