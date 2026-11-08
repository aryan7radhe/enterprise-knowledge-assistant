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

print("Tables: departments(dept_id, dept_name)")
print("        employees(emp_id, name, salary, dept_id, manager_id)")
print("Apni query likho (ek line me). Band karne ke liye: exit")
while True:
    try:
        q = input("\nSQL> ").strip()
    except EOFError:
        break
    if q.lower() in ("exit", "quit"):
        break
    if not q:
        continue
    try:
        cur = db.execute(q)
        if cur.description:
            print(" | ".join(c[0] for c in cur.description))
            for row in cur.fetchall():
                print(" | ".join(str(x) for x in row))
        else:
            db.commit()
            print("OK")
    except Exception as e:
        print("Error:", e)
