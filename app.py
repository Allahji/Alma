# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
import model

# -- Initialization section --
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Alma_User_Data'
app.config['MONGO_URI'] = 'mongodb+srv://admin:l4u59i5gQ92CQlk5@alma-data.x4yw1.mongodb.net/Alma_User_Data?retryWrites=true&w=majority'
mongo = PyMongo(app)

error_404 = "<title>404 Error</title><br><br><br><br><br><br><br><br><h1 style='text-align: center;'>404 error</h1>"

error_domain = "<title>Domain Error</title><br><br><br><br><br><br><br><br><div style='text-align: center;'><h1>Make sure to add a domain to your email and try again!</h1><br><br><p style = 'font-size: x-large;'>(youremail<u>.com</u>, youremail<u>.org</u>, youremail<u>.edu</u>)</p></div>"

# -- Routes section --


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/survey')
def survey():
    return render_template('survey.html')


@app.route('/survey/confirmation', methods=["GET", "POST"])
def survey_confirmation():
    email = request.form["email"]
    if len(email) == 0:
        email = ""
    return render_template('survey_confirmation.html', email=email, a1=request.form["a1"], a2=request.form["a2"], a3=request.form["a3"], a4=request.form["a4"], a5=request.form["a5"], a6=request.form["a6"])


@app.route('/survey/results', methods=["GET", "POST"])
def survey_results():
    if request.method == "POST":
        survey_responses = mongo.db.Survey_Responses
        email = request.form["email"]
        if len(email) == 0:
            email = "anonymous"
        if email == "anonymous" or model.domain_checker(email) == True:
            survey_responses.insert({
                "Email": email,
                "How often?": request.form["a1"],
                "Last time?": request.form["a2"],
                "What to change?": request.form["a3"],
                "Frustrates you?": request.form["a4"],
                "Healthy access?": request.form["a5"],
                "Delivery option?": request.form["a6"]
            })
            return render_template("survey_results.html")
        else:
            return error_domain
    else:
        return error_404

@app.route('/sign_up/confirmation', methods=["GET", "POST"])
def sign_up_confirmation():
    return render_template('sign_up_confirmation.html', name=request.form["name"], email=request.form["email"])

@app.route('/sign_up/results', methods=["GET", "POST"])
def sign_up_results():
    if request.method == "POST":
        email = request.form["email"]
        if model.domain_checker(email) == True:
            signed_up = mongo.db.Sign_Up
            signed_up.insert({
                "Name": request.form["name"].capitalize(),
                "Email": email
            })
            return render_template("sign_up_results.html")
        else:
            return error_domain
    else:
        return error_404

@app.route('/inquiry/confirmation', methods=["GET", "POST"])
def inquiry_confirmation():
    return render_template('inquiry_confirmation.html', name=request.form["name"], email=request.form["email"], inquiry=request.form["inquiry"])

@app.route('/inquiry/results', methods=["GET", "POST"])
def inquiry_results():
    if request.method == "POST":
        email = request.form["email"]
        if model.domain_checker(email) == True:
            inquiries = mongo.db.Inquiries
            inquiries.insert({
                "Name": request.form["name"].capitalize(),
                "Email": email,
                "Inquiry": request.form["inquiry"]
                })
            return render_template("inquiry_results.html")
        else:
            return error_domain
    else:
        return error_404