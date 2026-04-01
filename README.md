# Farmer–Crop–Instructor Training Management System
### Stack: Flask + Microsoft SQL Server (SSMS)

---

## Folder Structure

```
farmer_training_system/
├── app.py                  ← Flask backend (all routes)
├── requirements.txt        ← Python dependencies
├── database.sql            ← SQL Server schema + sample data
├── static/
│   └── styles.css
└── templates/
    ├── base.html
    ├── index.html
    ├── farmers.html / add_farmer.html
    ├── crops.html / add_crop.html
    ├── instructors.html / add_instructor.html
    ├── training.html / add_training.html
    └── farmer_training.html / assign_farmer_training.html
```

---

## Requirements

- Python 3.8+
- Microsoft SQL Server (any edition) + SSMS installed
- ODBC Driver 17 for SQL Server
- pip

---

## Setup (Step by Step)

### Step 1 — Install ODBC Driver 17 (if not already installed)

Download from Microsoft:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

Choose: **ODBC Driver 17 for SQL Server** → Windows x64

---

### Step 2 — Run the SQL script in SSMS

1. Open **SQL Server Management Studio (SSMS)**
2. Click **New Query**
3. Open `database.sql` and paste the entire contents into the query window
4. Click **Execute** (or press F5)

This will:
- Create the `farmer_training_db` database
- Create all 5 tables with relationships
- Insert sample data
- Show a row count summary to confirm success

---

### Step 3 — Configure the connection in app.py

Open `app.py` and find the `CONNECTION_STRING` section near the top.

**Windows Authentication (recommended — no password needed):**
```python
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=farmer_training_db;"
    "Trusted_Connection=yes;"
)
```

If your SQL Server instance has a name (common with Express edition), use:
```python
"SERVER=DESKTOP-YOURPC\\SQLEXPRESS;"
```
To find your server name: open SSMS → the server name shown in the login dialog is what you need.

**SQL Server Authentication (if you use a username/password):**
```python
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=farmer_training_db;"
    "UID=your_username;"
    "PWD=your_password;"
)
```

---

### Step 4 — Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Run the app

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

---

### Step 6 — Open in browser

Visit: **http://localhost:5000**

---

## Modules & Routes

| Module         | View URL                   | Add URL                          |
|----------------|----------------------------|----------------------------------|
| Farmers        | /farmers                   | /farmers/add                     |
| Crops          | /crops                     | /crops/add                       |
| Instructors    | /instructors               | /instructors/add                 |
| Training       | /training                  | /training/add                    |
| Attendance     | /farmer-training           | /farmer-training/assign          |

---

## Key Differences vs MySQL version

| Feature          | MySQL version          | SQL Server version           |
|------------------|------------------------|------------------------------|
| Driver           | mysql-connector-python | pyodbc                       |
| Placeholders     | `%s`                   | `?`                          |
| Auto-increment   | `AUTO_INCREMENT`       | `IDENTITY(1,1)`              |
| Date format      | native                 | `CONVERT(VARCHAR, date, 23)` |
| String concat    | `CONCAT(a, b)`         | `a + b`                      |
| Auth option      | user/password only     | Windows Auth or SQL Auth     |
