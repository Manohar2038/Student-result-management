# Student-result-management
# 🎓 Student Result Management REST API

A production-ready RESTful API built with **Python Flask** and **MySQL** to manage academic records through full CRUD operations. Features normalized database schemas, advanced SQL queries, stored procedures, and atomic transactions.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| Framework | Flask 3.0 |
| Database | MySQL 8.0 |
| DB Driver | PyMySQL |
| Config | python-dotenv |
| Testing | Postman |
| Version Control | Git |

---

## 📁 Project Structure

```
student-result-api/
├── app/
│   ├── __init__.py           # App factory, DB connection
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── students.py       # CRUD endpoints
│   │   └── reports.py        # Advanced SQL endpoints
│   ├── models/
│   │   └── db.py             # Reusable DB helper functions
│   └── utils/
│       └── validators.py     # Request payload validators
├── sql/
│   └── schema.sql            # Full DB schema + sample data
├── .env                      # Environment variables (not committed)
├── .gitignore
├── config.py                 # Flask config from .env
├── requirements.txt
├── run.py                    # Entry point
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/student-result-api.git
cd student-result-api
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Open MySQL Workbench or MySQL shell and run:

```bash
# Windows CMD
mysql -u root -p < sql\schema.sql

# Windows PowerShell
Get-Content sql\schema.sql | mysql -u root -p

# Mac / Linux
mysql -u root -p < sql/schema.sql
```

Or inside the MySQL shell:
```sql
source /full/path/to/sql/schema.sql
```

### 5. Configure environment variables

Create a `.env` file in the root directory:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=student_db
SECRET_KEY=your_secret_key
```

### 6. Run the server

```bash
python run.py
```

Server starts at: `http://localhost:5000`

---

## 🔗 API Endpoints

### Student CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/students` | Get all students (supports filters) |
| GET | `/api/v1/students/<id>` | Get a single student with subjects |
| POST | `/api/v1/students` | Add a new student |
| PUT | `/api/v1/students/<id>/results` | Update student GPA and grade |
| DELETE | `/api/v1/students/<id>` | Delete student (CASCADE) |

### Query Parameters for GET /students

| Param | Type | Example |
|-------|------|---------|
| `dept` | string | `?dept=CSE` |
| `semester` | integer | `?semester=5` |
| `sort_by` | string | `?sort_by=gpa` |

### Advanced SQL Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/reports/full` | Multi-table JOIN report |
| GET | `/api/v1/reports/above-avg` | Correlated subquery — above dept avg |
| POST | `/api/v1/batch/grade-update` | Stored procedure — batch recalculate |
| PUT | `/api/v1/batch/bulk-update` | Atomic bulk update with COMMIT/ROLLBACK |

---

## 📦 Request & Response Examples

### POST /api/v1/students

**Request Body:**
```json
{
  "name": "Arjun Sharma",
  "roll_number": "CS2301",
  "department": "CSE",
  "semester": 5
}
```

**Response:**
```json
{
  "status": "created",
  "message": "Student added successfully",
  "data": {
    "id": 1,
    "name": "Arjun Sharma",
    "roll_number": "CS2301",
    "department": "CSE",
    "semester": 5
  }
}
```

### PUT /api/v1/students/1/results

**Request Body:**
```json
{
  "gpa": 9.1,
  "grade": "A"
}
```

**Response:**
```json
{
  "status": "success",
  "transaction": "COMMIT",
  "data": {
    "student_id": 1,
    "gpa": 9.1,
    "grade": "A"
  }
}
```

### PUT /api/v1/batch/bulk-update

**Request Body:**
```json
[
  { "id": 1, "gpa": 9.5, "grade": "A" },
  { "id": 2, "gpa": 8.0, "grade": "B" }
]
```

**Response:**
```json
{
  "status": "committed",
  "rows_affected": 2,
  "transaction": "COMMIT"
}
```

---

## 🗄️ Database Schema

```
students       → results       (one-to-one, FK: student_id, CASCADE DELETE)
students       → enrollments   (one-to-many, FK: student_id)
subjects       → enrollments   (one-to-many, FK: subject_id)
students       → marks_detail  (one-to-many, FK: student_id)
subjects       → marks_detail  (one-to-many, FK: subject_id)
```

5 normalized tables — 3NF compliant with primary keys, foreign keys, and NOT NULL constraints.

---

## 🧠 Advanced SQL Features

- **Multi-table JOINs** — 5-table JOIN across students, results, enrollments, subjects, marks
- **Correlated Subqueries** — compare each student's GPA against their department average
- **Stored Procedure** — `recalculate_grades()` uses a cursor loop for batch processing
- **Transactions** — `START TRANSACTION` with `COMMIT` on success and `ROLLBACK` on failure for atomic bulk updates

---

## ✅ Validation Rules

| Field | Rule |
|-------|------|
| `name` | Required, non-empty string |
| `roll_number` | Required, unique |
| `department` | Required |
| `semester` | Required, integer between 1 and 8 |
| `gpa` | Float between 0.0 and 10.0 |
| `grade` | One of: A, B, C, D, F |

---

## 🔒 Error Responses

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Resource created |
| 204 | Deleted (no content) |
| 400 | Bad request / validation error |
| 404 | Resource not found |
| 500 | Server error / ROLLBACK triggered |

---

## 🧪 Testing with Postman

1. Open Postman
2. Set base URL to `http://localhost:5000`
3. Set `Content-Type: application/json` header for POST and PUT requests
4. Import and test each endpoint listed above

---

## 📌 Git Version Control

```bash
git init
git add .
git commit -m "feat: initial Student Result Management API"
git branch -M main
git remote add origin https://github.com/your-username/student-result-api.git
git push -u origin main
```

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-linkedin)

---

## 📄 License

This project is licensed under the MIT License.
