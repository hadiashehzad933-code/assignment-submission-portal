
import os
import sqlite3
from urllib.parse import urlparse

from flask import Flask, request, render_template_string, g


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="assignment-portal-secret",
        DATABASE=os.path.join(app.instance_path, "submissions.db")
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Create database and table
    with sqlite3.connect(app.config["DATABASE"]) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                registration_number TEXT NOT NULL,
                assignment_title TEXT NOT NULL,
                submission_url TEXT NOT NULL
            )
        """)

    # Connect to database
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    # Close database connection
    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    # Validate submission URL
    def is_valid_url(url):
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ("http", "https")
                and bool(parsed.netloc)
                and "." in parsed.netloc
            )
        except ValueError:
            return False

    # Main portal page
    @app.route("/", methods=["GET", "POST"])
    def home():
        error = None
        success = None

        if request.method == "POST":

            name = request.form.get("name", "").strip()
            registration = request.form.get(
                "registration_number", ""
            ).strip()
            title = request.form.get(
                "assignment_title", ""
            ).strip()
            url = request.form.get(
                "submission_url", ""
            ).strip()

            # Check required fields
            if not all([name, registration, title, url]):
                error = "All fields are required."

            # Check URL
            elif not is_valid_url(url):
                error = "Please enter a valid submission URL."

            else:
                db = get_db()

                db.execute("""
                    INSERT INTO submissions
                    (name, registration_number,
                     assignment_title, submission_url)
                    VALUES (?, ?, ?, ?)
                """, (name, registration, title, url))

                db.commit()
                success = "Assignment submitted successfully!"

        # Display saved submissions
        db = get_db()
        submissions = db.execute(
            "SELECT * FROM submissions ORDER BY id DESC"
        ).fetchall()

        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Assignment Submission Portal</title>
            <style>
                body {
                    font-family: Arial;
                    background: #f2f4f8;
                    margin: 40px;
                }

                .container {
                    max-width: 850px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }

                h1, h2 {
                    color: #243b64;
                }

                input {
                    width: 100%;
                    padding: 12px;
                    margin: 8px 0 16px;
                    box-sizing: border-box;
                }

                button {
                    background: #2457a6;
                    color: white;
                    padding: 12px 25px;
                    border: none;
                    cursor: pointer;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }

                th, td {
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                    overflow-wrap: anywhere;
                }

                th {
                    background: #e8edf5;
                }

                .error {
                    color: red;
                }

                .success {
                    color: green;
                }
            </style>
        </head>

        <body>
        <div class="container">

            <h1>Assignment Submission Portal</h1>

            <h2>Submit Your Assignment</h2>

            {% if error %}
                <p class="error">{{ error }}</p>
            {% endif %}

            {% if success %}
                <p class="success">{{ success }}</p>
            {% endif %}

            <form method="POST">

                <label>Student Name</label>
                <input type="text" name="name"
                       placeholder="Enter your name">

                <label>Registration Number</label>
                <input type="text" name="registration_number"
                       placeholder="Enter registration number">

                <label>Assignment Title</label>
                <input type="text" name="assignment_title"
                       placeholder="Enter assignment title">

                <label>Submission URL</label>
                <input type="text" name="submission_url"
                       placeholder="https://example.com">

                <button type="submit">Submit Assignment</button>

            </form>

            <h2>Saved Submissions</h2>

            <table>
                <tr>
                    <th>Name</th>
                    <th>Registration No.</th>
                    <th>Assignment</th>
                    <th>Submission URL</th>
                </tr>

                {% for item in submissions %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.registration_number }}</td>
                    <td>{{ item.assignment_title }}</td>
                    <td>
                        <a href="{{ item.submission_url }}"
                           target="_blank" rel="noopener noreferrer">
                           Open Submission
                        </a>
                    </td>
                </tr>
                {% endfor %}

            </table>

        </div>
        </body>
        </html>
        """, error=error, success=success,
        submissions=submissions)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
