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
    <h2>Change Password (Part B - Vulnerable UPDATE)</h2>
    <form method="POST">
        EID: <input type="text" name="eid"><br><br>
        Old Password: <input type="text" name="old_password"><br><br>
        New Password: <input type="text" name="new_password"><br><br>
        <input type="submit" value="Submit">
    </form>
    """

    if request.method == "POST":
        eid = request.form["eid"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        # VULNERABLE: user input directly concatenated into UPDATE query
        query = "UPDATE employee SET password = '" + new_password + "' " \
                "WHERE eid = '" + eid + "' AND password = '" + old_password + "'"

        injected_query = f"<h3>SQL Sent to Database:</h3><code>{query}</code>"

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            result = f"<p>Rows updated: {cursor.rowcount}</p>"
        except Exception as e:
            result = f"<p>Error: {e}</p>"

    return form_html + injected_query + result

app.run(debug=True, port=5001)