from flask import render_template, request, redirect, url_for, session, send_file
from app import app
from models import db, User, Prediction

import cv2
import mediapipe as mp
import os

from datetime import datetime

from gemini_service import analyze_palm, analyze_tarot

from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================

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

                return redirect(url_for("dashboard"))

            else:
                return "Wrong Password"

        return "User Not Found"

    return render_template("login.html")


# =========================================================
# REGISTER
# =========================================================

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

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:
            return "Username already exists. Please choose another username."

        existing_email = User.query.filter_by(
            email=email
        ).first()

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

        print("User registered successfully")

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if "user_email" not in session:
        return redirect(url_for("login"))

    return render_template(
        "profile.html",

        name=session.get("user_name"),

        email=session.get("user_email"),

        personality=session.get(
            "personality",
            "Please analyze your palm first."
        ),

        recommendation=session.get(
            "recommendation",
            "Please analyze your palm first."
        ),

        trend=session.get(
            "trend",
            "Please analyze your palm first."
        )
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# UPLOAD PALM IMAGE
# =========================================================

@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return "No image selected"

    image = request.files["image"]

    if image.filename == "":
        return "No image selected"

    os.makedirs("static", exist_ok=True)

    filepath = os.path.join(
        "static",
        image.filename
    )

    image.save(filepath)

    session["uploaded_image"] = image.filename

    return redirect(url_for("analyze"))


# =========================================================
# PALM ANALYSIS
# =========================================================

@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    filename = session.get("uploaded_image")

    if not filename:
        return "Please upload a palm image first."

    image_path = os.path.join(
        "static",
        filename
    )

    image = cv2.imread(image_path)

    if image is None:
        return "Unable to read the uploaded image."

    # -----------------------------------------------------
    # MediaPipe Hand Detection
    # -----------------------------------------------------

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.3
    )

    image = cv2.flip(image, 1)

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:

        message = "Hand Detected Successfully!"

    else:

        message = "No Hand Detected!"

    # -----------------------------------------------------
    # AI Prompt
    # -----------------------------------------------------

    prompt = f"""
You are an expert AI Palm Reader.

The hand detection result is:
{message}

Give the palm reading in this format:

Life:
Career:
Love:
Fortune:
Personality:
Recommendation:
Life Trend:

Keep each section concise (2-3 lines), positive,
and return the output exactly in the format above
without changing the headings.
"""

    # -----------------------------------------------------
    # Gemini Palm Analysis
    # -----------------------------------------------------

    prediction = analyze_palm(
        prompt,
        image_path
    )

    # -----------------------------------------------------
    # Save prediction in session
    # -----------------------------------------------------

    session["life"] = prediction.get(
        "life",
        "No life reading available."
    )

    session["career"] = prediction.get(
        "career",
        "No career reading available."
    )

    session["love"] = prediction.get(
        "love",
        "No love reading available."
    )

    session["fortune"] = prediction.get(
        "fortune",
        "No fortune reading available."
    )

    session["personality"] = prediction.get(
        "personality",
        "No personality analysis available."
    )

    session["recommendation"] = prediction.get(
        "recommendation",
        "No recommendation available."
    )

    session["trend"] = prediction.get(
        "life trend",
        "No life trend available."
    )

    session["health"] = prediction.get(
        "health",
        "Healthy"
    )

    session["wealth"] = prediction.get(
        "fortune",
        "Growing"
    )

    # -----------------------------------------------------
    # Save last prediction
    # -----------------------------------------------------

    session["last_prediction"] = prediction

    # -----------------------------------------------------
    # Save Palm Reading in Database
    # -----------------------------------------------------

    new_prediction = Prediction(

        user_email=session["user_email"],

        image_name=filename,

        prediction_type="Palm",

        life=session["life"],

        career=session["career"],

        love=session["love"],

        fortune=session["fortune"]
    )

    db.session.add(new_prediction)

    db.session.commit()

    return render_template(
    "result.html",
    prediction=prediction,
    filename=filename
)


# =========================================================
# REPORT PAGE
# =========================================================

@app.route("/report")
def report():

    if "user_email" not in session:
        return redirect(url_for("login"))

    prediction = session.get(
        "last_prediction"
    )

    filename = session.get(
        "uploaded_image"
    )

    return render_template(
        "report.html",

        prediction=prediction,

        filename=filename
    )


# =========================================================
# TAROT
# =========================================================

@app.route("/tarot", methods=["GET", "POST"])
def tarot():

    if "user_email" not in session:
        return redirect(url_for("login"))

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

        prediction = analyze_tarot(
            prompt
        )

        session["card"] = card

        session["tarot_result"] = prediction

        # -------------------------------------------------
        # Save Tarot Reading
        # -------------------------------------------------

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

    return render_template(
        "tarot.html"
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    if "user_email" not in session:
        return redirect(url_for("login"))

    predictions = Prediction.query.filter_by(

        user_email=session["user_email"]

    ).order_by(

        Prediction.id.desc()

    ).all()

    return render_template(
        "history.html",

        predictions=predictions
    )


# =========================================================
# DELETE HISTORY
# =========================================================

@app.route("/delete_history/<int:id>")
def delete_history(id):

    if "user_email" not in session:
        return redirect(url_for("login"))

    prediction = Prediction.query.get_or_404(id)

    # Only allow the logged-in user to delete their own reading
    if prediction.user_email != session["user_email"]:
        return "Unauthorized"

    db.session.delete(prediction)

    db.session.commit()

    return redirect(
        url_for("history")
    )


# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================

@app.route("/download_report")
def download_report():

    if "user_email" not in session:
        return redirect(url_for("login"))

    pdf_name = "Palmistry_Report.pdf"

    doc = SimpleDocTemplate(
        pdf_name
    )

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "<b>Palmistry & Tarot Intelligence Report</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "<br/>",
            styles["Normal"]
        )
    )

    # -----------------------------------------------------
    # Palm Image
    # -----------------------------------------------------

    filename = session.get(
        "uploaded_image"
    )

    if filename:

        image_path = os.path.join(
            "static",
            filename
        )

        if os.path.exists(image_path):

            img = Image(
                image_path
            )

            img.drawWidth = 120

            img.drawHeight = 120

            story.append(img)

    story.append(
        Paragraph(
            "<br/>",
            styles["Normal"]
        )
    )

    # -----------------------------------------------------
    # User Details
    # -----------------------------------------------------

    story.append(
        Paragraph(
            f"<b>Name:</b> {session.get('user_name')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Email:</b> {session.get('user_email')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> "
            f"{datetime.now().strftime('%d-%m-%Y')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Time:</b> "
            f"{datetime.now().strftime('%I:%M %p')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Report ID:</b> "
            f"PTR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<br/>",
            styles["Normal"]
        )
    )

    # -----------------------------------------------------
    # Palm Results
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "<b>Palm Reading Results</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "<br/>",
            styles["Normal"]
        )
    )

    if session.get("life"):

        story.append(
            Paragraph(
                f"<b>Life:</b> "
                f"{session.get('life')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Career:</b> "
                f"{session.get('career')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Love:</b> "
                f"{session.get('love')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Fortune:</b> "
                f"{session.get('fortune')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Personality:</b> "
                f"{session.get('personality')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Recommendation:</b> "
                f"{session.get('recommendation')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Life Trend:</b> "
                f"{session.get('trend')}",
                styles["BodyText"]
            )
        )

    else:

        story.append(
            Paragraph(
                "No palm analysis available.",
                styles["BodyText"]
            )
        )

    # -----------------------------------------------------
    # Build PDF
    # -----------------------------------------------------

    doc.build(story)

    return send_file(
        pdf_name,
        as_attachment=True
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_email" not in session:
        return redirect(url_for("login"))

    # -----------------------------------------------------
    # Overall Statistics
    # -----------------------------------------------------

    total_users = User.query.count()

    total_palm = Prediction.query.filter_by(
        prediction_type="Palm"
    ).count()

    total_tarot = Prediction.query.filter_by(
        prediction_type="Tarot"
    ).count()

    total_reports = Prediction.query.count()

    # -----------------------------------------------------
    # Current User Statistics
    # -----------------------------------------------------

    user_email = session["user_email"]

    user_palm = Prediction.query.filter_by(

        user_email=user_email,

        prediction_type="Palm"

    ).count()

    user_tarot = Prediction.query.filter_by(

        user_email=user_email,

        prediction_type="Tarot"

    ).count()

    user_total = Prediction.query.filter_by(

        user_email=user_email

    ).count()

    # -----------------------------------------------------
    # Dashboard
    # -----------------------------------------------------

    return render_template(

        "dashboard.html",

        name=session.get(
            "user_name"
        ),

        email=session.get(
            "user_email"
        ),

        # Personal analysis

        personality=session.get(
            "personality",
            "Please analyze your palm first."
        ),

        recommendation=session.get(
            "recommendation",
            "Please analyze your palm first."
        ),

        career=session.get(
            "career",
            "Please analyze your palm first."
        ),

        love=session.get(
            "love",
            "Please analyze your palm first."
        ),

        health=session.get(
            "health",
            "Excellent"
        ),

        wealth=session.get(
            "wealth",
            "Growing"
        ),

        # User analytics

        user_palm=user_palm,

        user_tarot=user_tarot,

        user_total=user_total,

        # Overall analytics

        total_users=total_users,

        total_palm=total_palm,

        total_tarot=total_tarot,

        total_reports=total_reports
    )