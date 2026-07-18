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

if __name__ == '__main__':
    app.run(debug=True)