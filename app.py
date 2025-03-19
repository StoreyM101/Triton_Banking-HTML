import os
from flask import Flask, render_template, request, redirect, url_for, session
#   1) Flask - The micro web development framework for building webpages
#   2) render_template - uses the render HTML templates using Jinja2 to generate dynamic HTML templates which allow for Python variables to be integrated into HTML webpages
#   3) request - used to handle incoming data/user requests to applications (like a form submission or URL query). This is stored in request object.
#   4) redirect - used to redirect the user to a different URL when necessary.
#   5) url_for - used to dynamically generate the correct URL for any route in the Flask app.
#   6) session - used to maintain webpage persistence, storing data between requests.

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Key for session handling.

# Data Dictionary for all information displayed to dashboard.
fake_users = { # Dashboard Information
    "doej123": {
        "password": "lotsodough25?",
        "name": "John Doe",
        "account_balance": "£5,200.00",
        "transactions": [ # Start of transactions list
            "Deposit: + £1,000",
            "Amazon Purchase: - £120",
            "Utility Bill: - £80",
            "Wagamamas: - £32",
            "Adam Cross: + £45",
            "Tesco Express: - £15",
            "Boss: + £350"  
        ], # End of transactions list
        "credit_card": { # Start credit_card details
            "number": "5678 0172 9999 1234",
            "expiry_date": "12/26"
        } # End of credit_card details
    }
}

#_____________________________________________________________First Route (Login)_____________________________________________________________

@app.route("/", methods=["GET", "POST"]) # Defines the route for the Login page. Allows for HTTP GET and POST methods

def login(): # Define Login Function
    if request.method == "POST": # If the request method is a HTTP POST request, it means that the user submitted a form.
        username = request.form["uname"] # Verifies Username Input
        password = request.form["psw"] # Verifies Password Input

        if username in fake_users and fake_users[username]["password"] == password: # if input matches dictionary.
            session["username"] = username  # The username is stored within the session
            return redirect(url_for("dashboard")) # User is redirected to dashboard
        else:
            return "Invalid credentials, please try again.", 401 # Present error 401 (Unauthorised client error response)
  
    return render_template("Login.html") # Displays login form using GET request.

#_____________________________________________________________Second Route (Banking Dashboard)_____________________________________________________________

@app.route("/dashboard") # Defines the route for the Dashboard page.

def dashboard():
    if "username" not in session: # If username is not logged in the session
        return redirect(url_for("login"))  # Redirects back to login page

    user_data = fake_users.get(session["username"]) # Retrieves user data from Dictionary
    if user_data: # If Data exists
        return render_template("Dashboard.html", user=user_data) # Passes user data to Dashboard
    else:
        return redirect(url_for("login")) # Redirects back to login if user not found

#_____________________________________________________________Third Route (Logout)_____________________________________________________________

@app.route("/logout", methods=["POST"]) # Defines the route for when a user logs out. Allows for HTTP POST (used for resource creation) method.

def logout(): # Defines Logout Function
    session.pop("username", None)  # Remove user from session
    return redirect(url_for("login")) # Redirects users back to login screen

if __name__ == "__main__": # ensures script runs only when executed directly
    app.run(debug=True) # enables auto-reload on code changes
