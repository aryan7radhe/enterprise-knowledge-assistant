import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER,
    dept_id INTEGER, manager_id INTEGER
);
INSERT INTO departments VALUES (1,'IT'), (2,'HR'), (3,'Finance'), (4,'Admin');
INSERT INTO employees VALUES
 (1,'Asha',50000,1,NULL),
 (2,'Ravi',60000,1,1),
 (3,'Meera',45000,2,1),
 (4,'Karan',70000,1,1),
 (5,'Sana',45000,3,1),
 (6,'Dev',55000,3,5),
 (7,'Isha',40000,NULL,NULL);
""")

LESSONS = [
    ("1. WHERE + ORDER BY: 50000 se zyada salary, bade se chhota",
     "SELECT name, salary FROM employees WHERE salary > 50000 ORDER BY salary DESC;"),
    ("2. GROUP BY: har department me kitne log aur average salary",
     "SELECT dept_id, COUNT(*) AS total, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id;"),
    ("3. HAVING: sirf wo department jahan 1 se zyada log hain",
     "SELECT dept_id, COUNT(*) AS total FROM employees GROUP BY dept_id HAVING COUNT(*) > 1;"),
    ("4. INNER JOIN: sirf wo employees jinka department hai",
     "SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.dept_id;"),
    ("5. LEFT JOIN: saare departments, chahe koi employee na ho (Admin dekho)",
     "SELECT d.dept_name, COUNT(e.emp_id) AS total FROM departments d LEFT JOIN employees e ON d.dept_id = e.dept_id GROUP BY d.dept_name;"),
    ("6. Second highest salary",
     "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);"),
    ("7. Average se zyada salary wale (subquery)",
     "SELECT name, salary FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);"),
    ("8. SELF JOIN: employee ke saath uske manager ka naam",
     "SELECT e.name AS employee, m.name AS manager FROM employees e LEFT JOIN employees m ON e.manager_id = m.emp_id;"),
    ("9. Duplicate salary dhoondhna",
     "SELECT salary, COUNT(*) AS times FROM employees GROUP BY salary HAVING COUNT(*) > 1;"),
    ("10. NULL ka jaal: COUNT(*) vs COUNT(column)",
     "SELECT COUNT(*) AS count_star, COUNT(dept_id) AS count_dept FROM employees;"),
]

for title, sql in LESSONS:
    print("=" * 70)
    print(title)
    print("SQL:", sql)
    cur = db.execute(sql)
    cols = [c[0] for c in cur.description]
    print("  ", " | ".join(cols))
    for row in cur.fetchall():
        print("  ", " | ".join(str(x) for x in row))
print("=" * 70)
