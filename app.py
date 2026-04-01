# ============================================================
# app.py — Flask Backend
# Farmer-Crop-Instructor Training Management System
# Database: Microsoft SQL Server (SSMS)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = "farmer_training_secret"

# -----------------------------------------------
# SQL Server Configuration — update these values
# -----------------------------------------------
# Option A: Windows Authentication (most common with SSMS)
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"           # or e.g. DESKTOP-ABC\\SQLEXPRESS
    "DATABASE=farmer_training_db;"
    "Trusted_Connection=yes;"
)

# Option B: SQL Server Authentication (username + password)
# CONNECTION_STRING = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=localhost;"
#     "DATABASE=farmer_training_db;"
#     "UID=your_sql_username;"
#     "PWD=your_sql_password;"
# )

def get_db():
    """Return a new SQL Server connection via pyodbc."""
    return pyodbc.connect(CONNECTION_STRING)

def rows_to_dicts(cursor):
    """Convert pyodbc cursor rows into a list of dicts."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# ============================================================
# HOME
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# FARMERS
# ============================================================
@app.route("/farmers")
def farmers():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT FarmerID, Name, Village, Phone, LandArea FROM Farmers ORDER BY FarmerID DESC")
    rows = rows_to_dicts(cur)
    conn.close()
    return render_template("farmers.html", farmers=rows)


@app.route("/farmers/add", methods=["GET", "POST"])
def add_farmer():
    if request.method == "POST":
        name      = request.form["name"]
        village   = request.form["village"]
        phone     = request.form["phone"]
        land_area = request.form["land_area"]
        conn = get_db()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO Farmers (Name, Village, Phone, LandArea) VALUES (?, ?, ?, ?)",
            (name, village, phone, land_area)
        )
        conn.commit()
        conn.close()
        flash("Farmer added successfully!", "success")
        return redirect(url_for("farmers"))
    return render_template("add_farmer.html")


# ============================================================
# CROPS
# ============================================================
@app.route("/crops")
def crops():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT CropID, CropName, Season FROM Crops ORDER BY CropID DESC")
    rows = rows_to_dicts(cur)
    conn.close()
    return render_template("crops.html", crops=rows)


@app.route("/crops/add", methods=["GET", "POST"])
def add_crop():
    if request.method == "POST":
        crop_name = request.form["crop_name"]
        season    = request.form["season"]
        conn = get_db()
        cur  = conn.cursor()
        cur.execute("INSERT INTO Crops (CropName, Season) VALUES (?, ?)", (crop_name, season))
        conn.commit()
        conn.close()
        flash("Crop added successfully!", "success")
        return redirect(url_for("crops"))
    return render_template("add_crop.html")


# ============================================================
# INSTRUCTORS
# ============================================================
@app.route("/instructors")
def instructors():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT InstructorID, Name, Specialization, Organization FROM Instructors ORDER BY InstructorID DESC")
    rows = rows_to_dicts(cur)
    conn.close()
    return render_template("instructors.html", instructors=rows)


@app.route("/instructors/add", methods=["GET", "POST"])
def add_instructor():
    if request.method == "POST":
        name           = request.form["name"]
        specialization = request.form["specialization"]
        organization   = request.form["organization"]
        conn = get_db()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO Instructors (Name, Specialization, Organization) VALUES (?, ?, ?)",
            (name, specialization, organization)
        )
        conn.commit()
        conn.close()
        flash("Instructor added successfully!", "success")
        return redirect(url_for("instructors"))
    return render_template("add_instructor.html")


# ============================================================
# TRAINING SESSIONS
# ============================================================
@app.route("/training")
def training():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""
        SELECT t.TrainingID, c.CropName, i.Name AS InstructorName,
               CONVERT(VARCHAR, t.Date, 23) AS Date, t.Location
        FROM Training t
        JOIN Crops       c ON t.CropID       = c.CropID
        JOIN Instructors i ON t.InstructorID = i.InstructorID
        ORDER BY t.Date DESC
    """)
    rows = rows_to_dicts(cur)
    conn.close()
    return render_template("training.html", sessions=rows)


@app.route("/training/add", methods=["GET", "POST"])
def add_training():
    if request.method == "POST":
        crop_id       = request.form["crop_id"]
        instructor_id = request.form["instructor_id"]
        date          = request.form["date"]
        location      = request.form["location"]
        conn = get_db()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO Training (CropID, InstructorID, Date, Location) VALUES (?, ?, ?, ?)",
            (crop_id, instructor_id, date, location)
        )
        conn.commit()
        conn.close()
        flash("Training session created!", "success")
        return redirect(url_for("training"))

    # GET — load dropdowns
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT CropID, CropName, Season FROM Crops")
    crops = rows_to_dicts(cur)
    cur.execute("SELECT InstructorID, Name, Specialization FROM Instructors")
    instructors = rows_to_dicts(cur)
    conn.close()
    return render_template("add_training.html", crops=crops, instructors=instructors)


# ============================================================
# FARMER TRAINING — View Attendance
# ============================================================
@app.route("/farmer-training")
def farmer_training():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""
        SELECT f.Name  AS FarmerName,
               f.Village,
               c.CropName,
               CONVERT(VARCHAR, t.Date, 23) AS Date,
               t.Location,
               i.Name AS InstructorName
        FROM FarmerTraining ft
        JOIN Farmers     f ON ft.FarmerID    = f.FarmerID
        JOIN Training    t ON ft.TrainingID  = t.TrainingID
        JOIN Crops       c ON t.CropID       = c.CropID
        JOIN Instructors i ON t.InstructorID = i.InstructorID
        ORDER BY t.Date DESC
    """)
    rows = rows_to_dicts(cur)
    conn.close()
    return render_template("farmer_training.html", records=rows)


# ============================================================
# FARMER TRAINING — Assign Farmer
# ============================================================
@app.route("/farmer-training/assign", methods=["GET", "POST"])
def assign_farmer_training():
    # ── Handle form submission FIRST ──
    if request.method == "POST":
        farmer_id   = request.form["farmer_id"]
        training_id = request.form["training_id"]
        conn = get_db()
        cur  = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO FarmerTraining (FarmerID, TrainingID) VALUES (?, ?)",
                (int(farmer_id), int(training_id))
            )
            conn.commit()
            flash("Farmer assigned to training successfully!", "success")
        except pyodbc.Error as e:
            conn.rollback()
            # SQL Server error 2627 = unique constraint / primary key violation
            if "2627" in str(e) or "2601" in str(e):
                flash("This farmer is already assigned to that training session.", "warning")
            else:
                flash(f"Database error: {str(e)}", "error")
        finally:
            conn.close()
        return redirect(url_for("farmer_training"))

    # ── GET — load dropdowns ──
    conn = get_db()
    cur  = conn.cursor()

    cur.execute("SELECT FarmerID, Name, Village FROM Farmers ORDER BY Name")
    farmers = rows_to_dicts(cur)

    cur.execute("""
        SELECT t.TrainingID,
               CONVERT(VARCHAR, t.Date, 23)  AS Date,
               c.CropName,
               t.Location,
               i.Name AS InstructorName
        FROM Training t
        JOIN Crops       c ON t.CropID       = c.CropID
        JOIN Instructors i ON t.InstructorID = i.InstructorID
        ORDER BY t.Date DESC
    """)
    sessions = rows_to_dicts(cur)

    # Unique sorted dates for the date picker filter
    dates = sorted(set(s["Date"] for s in sessions))
    conn.close()

    return render_template("assign_farmer_training.html",
                           farmers=farmers, sessions=sessions, dates=dates)


# ============================================================
# Run
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
