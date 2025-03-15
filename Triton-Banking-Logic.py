import os
from flask import Flask, render_template, request, redirect, url_for, session # Imports the Python module known as Flask - a micro web development framework.
# There are a number of imported components here:
#   1) Flask - The micro web development framework for building webpages
#   2) render_template - uses the render HTML templates using Jinja2 to generate dynamic HTML templates which allow for Python variables to be integrated into HTML webpages
#   3) request - used to handle incoming data/user requests to applications (like a form submission or URL query). This is stored in request object.
#   4) redirect - used to redirect the user to a different URL when necessary.
#   5) url_for - used to dynamically generate the correct URL for any route in the Flask app.
#   6) session - used to maintain webpage persistence, storing data between requests.

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Defines a key needed for efficient session handling.

# Defines Data Dictionary which is pulled when a user opens success.html.
fake_users = { # This simulates a database of users (No actual Database is used properly here because this is simply a test with one valid user)
    "doej123": { # Username field
        "password": "lotsodough25?", # Password field
        "name": "John Doe", # Name of user field
        "account_balance": "£5,200.00", # Account Balance field
        "transactions": [ # List of transactions made in this bank account (+ = money sent in, - = money sent out)
            "Deposit: + £1,000",
            "Amazon Purchase: - £120",
            "Utility Bill: - £80",
            "Wagamamas: - £32",
            "Adam Cross: + £45",
            "Tesco Express: - £15",
            "Boss: + £350"  
        ], # End of transactions list
        "credit_card": { # This begins the definition of credit_card details
            "number": "5678 0172 9999 1234", # Credit card number field
            "expiry_date": "12/26" # Expiry date field
        } # Ends the definition of credit_card details
    }
}

#_____________________________________________________________First Route (Login)_____________________________________________________________

@app.route("/", methods=["GET", "POST"]) # Defines the route for the Login page. Allows for HTTP GET (used for data retrieval) and POST (used for resource creation) methods

def login():
    if request.method == "POST": # If the request method is a HTTP POST request, it means that the user submitted a form.
        username = request.form["uname"] # Retrieves the entered username provided by user
        password = request.form["psw"] # Retrieves the entered password provided by user

        if username in fake_users and fake_users[username]["password"] == password: # if the entered username/password is found within the fake_users dictionary.
            session["username"] = username  # The username is stored within the session
            return redirect(url_for("dashboard")) # User is redirected to dashboard
        else: #  # if the entered username/password is not found within the fake_users dictionary.
            return "Invalid credentials, please try again.", 401 # Present error 401 (Unauthorised client error response)
  
    return render_template("Login.html") # Displays login form using GET request.

#_____________________________________________________________Second Route (Banking Dashboard)_____________________________________________________________

@app.route("/dashboard") # Defines the route for the Dashboard page.

def dashboard():
    if "username" not in session: # If username is not logged in the session
        return redirect(url_for("login"))  # Redirects back to login page

    user_data = fake_users.get(session["username"]) # Retrieves user data from Dictionary
    if user_data: # If Data exists the move to next line
        return render_template("Dashboard.html", user=user_data) # Passes user data to success.html (Dashboard)
    else:  # If Data does not exist for user
        return redirect(url_for("login")) # Redirects back to login if user not found

#_____________________________________________________________Third Route (Logout)_____________________________________________________________

@app.route("/logout", methods=["POST"]) # Defines the route for when a user logs out. Allows for HTTP POST (used for resource creation) method.

def logout():
    session.pop("username", None)  # Remove user from session
    return redirect(url_for("login")) # Redirects users back to login screen

if __name__ == "__main__": # ensures script runs only when executed directly
    app.run(debug=True) # enables auto-reload on code changes