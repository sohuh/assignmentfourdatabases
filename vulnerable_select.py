from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # your MySQL Workbench password
        database="dbtest"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    injected_query = ""

    form_html = """
    <h2>Employee Lookup (Part A - Vulnerable SELECT)</h2>
    <form method="POST">
        EID: <input type="text" name="eid"><br><br>
        Password: <input type="text" name="password"><br><br>
        <input type="submit" value="Submit">
    </form>
    """

    if request.method == "POST":
        eid = request.form["eid"]
        password = request.form["password"]

        # VULNERABLE: user input directly concatenated into query
        query = "SELECT name, salary, ssn FROM employee " \
                "WHERE eid = '" + eid + "' AND password = '" + password + "'"

        injected_query = f"<h3>SQL Sent to Database:</h3><code>{query}</code>"

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                result = "<h3>Results:</h3><table border='1'><tr><th>Name</th><th>Salary</th><th>SSN</th></tr>"
                for row in rows:
                    result += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
                result += "</table>"
            else:
                result = "<p>No records found.</p>"
        except Exception as e:
            result = f"<p>Error: {e}</p>"

    return form_html + injected_query + result

app.run(debug=True)