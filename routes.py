from flask import render_template, request, redirect,url_for,session
from app import app
from models import db, User,Prediction
import cv2
import mediapipe as mp
from gemini_service import analyze_palm
from flask import redirect, url_for
from flask import session
from gemini_service import analyze_tarot
from sqlalchemy import text


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        print("Email:", email)
        print("Password:", password)
        print("User:", user)

        if user:
            if user.password == password:
             session["user_id"] = user.id
             session["user_name"] = user.fullname
             session["user_email"] = user.email
             return redirect("/profile")
            else:
                return "Wrong Password"

        return "User Not Found"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        fullname = request.form["fullname"]
        age_group = request.form["age_group"]
        interest = request.form["interest"]
        goal = request.form["goal"]
        reading_preference = request.form["reading_preference"]

        print(username, email, password)
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
         return "Username already exists. Please choose another username."

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
         return "Email already registered. Please use another email."

        user = User(
    username=username,
    email=email,
    password=password,
    fullname=fullname,
    age_group=age_group,
    interest=interest,
    goal=goal,
    reading_preference=reading_preference
)

        db.session.add(user)
        db.session.commit()

        users = User.query.all()
        print(users)
        for u in users:
         print(u.username, u.email, u.password)

        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/profile")
def profile():
    return render_template(
        "profile.html",
        name=session.get("user_name"),
        email=session.get("user_email")
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

from flask import session
import os

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]

    if image.filename == "":
        return "No image selected"

    filepath = os.path.join("static", image.filename)
    image.save(filepath)

    session["uploaded_image"] = image.filename

    return redirect("/analyze")
@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    filename = session.get("uploaded_image")
    image_path = os.path.join("static", filename)

    image = cv2.imread(image_path)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.3
    )

    image = cv2.flip(image, 1)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        message = "Hand Detected Successfully!"
    else:
        message = "No Hand Detected!"

    prompt = f"""
You are an expert AI Palm Reader.

The hand detection result is:
{message}

Give the palm reading in this format:

Life:
Career:
Love:
Fortune:

Keep each answer positive and within 2-3 lines.
"""

    prediction = analyze_palm(prompt, image_path)

    new_prediction = Prediction(
        user_email=session["user_email"],
        image_name=filename,
        life=prediction["life"],
        career=prediction["career"],
        love=prediction["love"],
        fortune=prediction["fortune"]
    )

    db.session.add(new_prediction)
    db.session.commit()

    session["last_prediction"]= prediction
    
    return render_template(
        "result.html",
        filename=filename,
        message=message,
        prediction=prediction
    )
@app.route("/report")
def report():
    prediction = session.get("last_prediction")
    filename = session.get("uploaded_image")

    return render_template(
        "report.html",
        prediction=prediction,
        filename=filename
    )
@app.route("/tarot", methods=["GET", "POST"])
def tarot():

    if request.method == "POST":

        card = request.form["card"]

        prompt = f"""
You are an expert AI Tarot Reader.

The selected tarot card is:
{card}

Give the reading in this format:

Meaning:
Love:
Career:
Advice:

Keep each answer positive and within 2-3 lines.
"""

        prediction = analyze_tarot(prompt)
        print(Prediction.__table__.columns.keys())
        print(Prediction)

        new_prediction = Prediction(
         user_email=session["user_email"],
         image_name="Tarot Reading",
         prediction_type="Tarot",
         input_data=card,
         result=prediction
)

        db.session.add(new_prediction)
        db.session.commit()

        return render_template(
            "tarot.html",
            prediction=prediction,
            selected_card=card
        )

    return render_template("tarot.html")
@app.route("/history")
def history():

    if "user_email" not in session:
        return redirect(url_for("login"))

    predictions = Prediction.query.filter_by(
        user_email=session["user_email"]
    ).order_by(Prediction.id.desc()).all()

    return render_template(
        "history.html",
        predictions=predictions
    )
@app.route("/delete_history/<int:id>")
def delete_history(id):
    prediction = Prediction.query.get_or_404(id)
    db.session.delete(prediction)
    db.session.commit()
    return redirect(url_for("history"))