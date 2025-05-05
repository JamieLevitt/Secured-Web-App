from flask import Flask, render_template, request, redirect, jsonify, session
from flask_session import Session
from flask_csp import CSP
import user_management as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__) 
app.config.update( # Used for SameSite Cookies (Prevents CSRF Attacks)
    SECRET_KEY = 'AJDLFKALDKBHAJFIHABJDKHBJagvjfouihigyuqbhajopidhuigyuvhjhjiuyigtfcghvjbkjiouyigftygyHUOJIHUIGYUVJBHKLIAOHU',
    SESSION_COOKIE_SAMESITE = 'Lax'
)

CSP(app, # App wide CSP Protection
    base_uri=["'self'"],
    default_src=["'self'"],
    style_src=["'self'"],
    script_src=["'self"],
    img_src=["*"],
    media_src=["'self'"],
    font_src=["'self'"],
    object_src=["'self'"],
    child_src=["'self'"],
    connect_src=["'self'"],
    worker_src=["'self'"],
    frame_src=["'none'"],
    frame_ancestors=["'none'"],
    form_action=["'self'"]
)

csp_ext = CSP()
 
# ---------------- Configuration ----------------
app.config["SESSION_PERMANENT"] = False     # Sessions expire when browser closes
app.config["SESSION_TYPE"] = "filesystem"     # Store session data on the filesystem
Session(app)

# @app.route("/")
# def index():
#     # If no username in session, redirect to login
#     if not session.get("name"):
#         return redirect("/login")
#     return render_template("index.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         # Record the user name in session
#         session["name"] = request.form.get("name")
#         return redirect("/")
#     return render_template("login.html")

# @app.route("/logout")
# def logout():
#     # Clear the username from session
#     session["name"] = None
#     return redirect("/")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if session.get("user", None):
        dbHandler.listFeedback()
        return redirect("/success")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        userData = dbHandler.retrieveUser(username)
        if userData:
            redirect("/")
        dbHandler.insertUser(username, password, DoB)
        return redirect("/success")
    else:
        return render_template("/signup.html")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if session.get("user", None):
        dbHandler.listFeedback()
        return redirect("/success")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        userData = dbHandler.retrieveUser(username)
        if userData:
            if password == userData["pass"]:
                session["user"] = username
                app.logger.warning(session["user"])
                return redirect("/success")
            else:
                return jsonify({"pass": password, "stored": userData["pass"]})
        else:
            return redirect("/")
    else:
        return render_template("/index.html")

@app.route("/success", methods=["POST", "GET"])
def addFeedback():
    app.logger.warning(session["user"])
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if not session.get("user", None):
        return redirect("/")
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value=session["user"])
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value=session["user"])

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
