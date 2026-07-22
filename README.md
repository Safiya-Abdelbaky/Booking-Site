# RC Workspace Booking System

<<<<<<< HEAD
This is a web application that allows users to seamlessly search, book, and manage workspace reservations (like Private rooms , OpenAir or Coworker spaces). It features user authentication, a dynamic search filter, and a dashboard to modify or cancel upcoming bookings.
=======
This is a web application that allows users to seamlessly search, book, and manage workspace reservations (like Private rooms or Coworker spaces). It features user authentication, a dynamic search filter, and a dashboard to modify or cancel upcoming bookings.
>>>>>>> 762eff4d66a3f5101fca12003d99e06996d0846e

The application implements an advanced backend validation logic (using datetime operations) to prevent time slot overlaps and past-date bookings, combined with a synchronized frontend experience utilizing JavaScript's DOM manipulation and localStorage to preserve user preferences across page reloads.

## Prerequisites
<<<<<<< HEAD

 Needs to install 

=======
 Needs to install
>>>>>>> 762eff4d66a3f5101fca12003d99e06996d0846e
* Flask (install via `pip install Flask`)

## Project Checklist

- [x] It is available on GitHub.

- [x] It uses the Flask web framework.

- [x] It uses at least one module from the Python Standard Library other than the random module.
Module name: `datetime`, `json`, and `os`

<<<<<<< HEAD
- [x] It contains at least one class written by you that has both properties and methods. 
=======
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes 
>>>>>>> 762eff4d66a3f5101fca12003d99e06996d0846e
File name for the class definition: `app.py`
Line number(s) for the class definition: 10
Name of two properties: `self.bookings_file` and `self.users_file`
Name of two methods: `save_booking()` and `update_booking()`
File name and line numbers where the methods are used: `app.py`, instantiated at line 46 (`manager = WorkspaceManager(...)`), and methods used at line 102 (`manager.register_user`), line 143 (`manager.get_bookings()`), and line 171 (`manager.save_booking`).

- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.

- [x] It uses modern JavaScript (for example, let and const rather than var).

- [x] It makes use of the reading and writing to the same file feature.

- [x] It contains conditional statements.
File name: `app.py`
Line number(s): 15 (`if not os.path.exists(self.bookings_file):`) and 86 (`if 'user' in session:`)

<<<<<<< HEAD
- [x] It contains loops. 
=======
- [x] It contains loops.
>>>>>>> 762eff4d66a3f5101fca12003d99e06996d0846e
File name: `app.py`
Line number(s): 26 (`for user in users:`) and 146 (`for room in all_rooms:`)

- [x] It lets the user enter a value in a text box at some point. This value is received and processed by your back end Python code.

- [x] It doesn't generate any error message even if the user enters a wrong input.

- [x] It is styled using your own CSS.

- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.

<<<<<<< HEAD
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
=======
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
>>>>>>> 762eff4d66a3f5101fca12003d99e06996d0846e
