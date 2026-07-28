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
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import os
from datetime import datetime
from reportlab.platypus import Image



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

    session["life"] = prediction["life"]
    session["career"] = prediction["career"]
    session["love"] = prediction["love"]
    session["fortune"] = prediction["fortune"]

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

        session["card"] = card
        session["tarot_result"] = prediction
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
@app.route("/download_report")
def download_report():

    pdf_name = "Palmistry_Report.pdf"

    doc = SimpleDocTemplate(pdf_name)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Palmistry & Tarot Intelligence Report</b>", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))
    image_path = os.path.join("static", session.get("uploaded_image"))

    if os.path.exists(image_path):
     img = Image(image_path)
     img.drawWidth = 120
     img.drawHeight = 120
     story.append(img)

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Name:</b> {session.get('user_name')}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Email:</b> {session.get('user_email')}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Time:</b> {datetime.now().strftime('%I:%M %p')}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Report ID:</b> PTR-{datetime.now().strftime('%Y%m%d%H%M%S')}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Palm Reading Results</b>", styles["Heading2"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    if session.get("life"):
     story.append(Paragraph(f"<b>Life:</b> {session['life']}", styles["BodyText"]))
     story.append(Paragraph(f"<b>Career:</b> {session['career']}", styles["BodyText"]))
     story.append(Paragraph(f"<b>Love:</b> {session['love']}", styles["BodyText"]))
     story.append(Paragraph(f"<b>Fortune:</b> {session['fortune']}", styles["BodyText"]))
     doc.build(story)

    return send_file(
    pdf_name,
    as_attachment=True
)