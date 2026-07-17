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
        self_users_file = users_file
        self._initialize_files()


    def _intialize_files(self):
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
        