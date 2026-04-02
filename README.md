# assignmentfourdatabases
To run the Python files in this, make sure you have the company database created by doing a command like: and make sure you have the MySQL connector Python extension installed:
CREATE DATABASE IF NOT EXISTS dbtest;
USE dbtest;

CREATE TABLE employee (
  eid VARCHAR(20),
  name VARCHAR(50),
  password VARCHAR(50),
  salary INT,
  ssn VARCHAR(20)
);

INSERT INTO employee VALUES ('EID5000', 'Alice', 'passwd123', 80000, '111-22-3333');
INSERT INTO employee VALUES ('EID5001', 'Bob',   'passwd456', 75000, '444-55-6666');
INSERT INTO employee VALUES ('EID5002', 'Charlie','passwd789', 90000, '777-88-9999');

Vulnerable_select:
To inject: Type EID5002'# in the EID box and anything in the Password box.
The # comments out the password check — you get Charlie's data without knowing his password.
Or type a' OR 1=1 # in EID to dump all employee records.

Vulnerable_update:
To inject: Log in as Alice (EID5000 / passwd123). In the New Password box, type:
passwd999', salary=999999 #
This turns the query into:
UPDATE employee SET password = 'passwd999', salary=999999 #' WHERE eid = ...
Alice just gave herself a raise without the form ever asking for salary!

safe_select:
Try the same injection: Type EID5002'# in EID — this time it returns nothing because the '# is treated as literal data, not SQL code.

Run these commands:
python vulnerable_select.py   # go to http://localhost:5000
python vulnerable_update.py   # go to http://localhost:5001
python safe_select.py   # go to http://localhost:5002

Screenshot: the form, what you typed in, the SQL it shows on screen, and the result from the database.
