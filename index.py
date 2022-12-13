import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('front.html', what='fear')

@app.route("/create")
def create():
	return render_template('create.html')

@app.route("/create", methods = ["POST"])
def rec_create():
	d = dict()
	d["First Name"] = request.form["first"]
	d["Last Name"] = request.form["last"]
	d["Major"] = request.form["major"]
	d["GPA"] = request.form["gpa"]
	d["ID"] = request.form["id"]
	connection = sqlite3.connect("students.db")
	crsr = connection.cursor()
	crsr.execute(f'INSERT INTO STUDENTS VALUES ("{d["First Name"]}", "{d["Last Name"]}", "{d["Major"]}", {int(d["GPA"])}, "{d["ID"]}")')
	connection.commit()
	crsr.close()
	connection.close()
	return render_template('created.html',data=d)

@app.route("/read")
def read():
	return render_template('read.html')

@app.route("/read", methods = ["POST"])
def re_read():
	query = request.form["id"]
	connection = sqlite3.connect("students.db")
	crsr = connection.cursor()
	crsr.execute(query)
	ans = crsr.fetchall()
	res = [list(i) for i in ans]
	crsr.close()
	connection.close()
	return render_template('read_.html',data=query, result=res)

@app.route("/update")
def update():
	return render_template('update.html')

@app.route("/update",methods = ["POST"])
def re_update():
	d = dict()
	d["First Name"] = request.form["first"]
	d["Last Name"] = request.form["last"]
	d["Major"] = request.form["major"]
	d["GPA"] = request.form["gpa"]
	d["ID"] = request.form["id"]
	connection = sqlite3.connect("students.db")
	crsr = connection.cursor()
	crsr.execute(f'UPDATE STUDENTS SET first_name = "{d["First Name"]}" WHERE id = "{int(d["ID"])}";')
	crsr.execute(f'UPDATE STUDENTS SET last_name = "{d["Last Name"]}" WHERE id = "{int(d["ID"])}";')
	crsr.execute(f'UPDATE STUDENTS SET major = "{d["Major"]}" WHERE id = "{int(d["ID"])}";')
	crsr.execute(f'UPDATE STUDENTS SET gpa = "{d["GPA"]}" WHERE id = "{int(d["ID"])}";')
	connection.commit()
	crsr.close()
	connection.close()
	return render_template('updated.html', data = d)

@app.route("/delete")
def delete():
	return render_template('delete.html')

@app.route("/delete", methods = ["POST"])
def re_delete():
	did = request.form["id"]
	connection = sqlite3.connect("students.db")
	crsr = connection.cursor()
	crsr.execute(f'SELECT * FROM STUDENTS WHERE id = {int(did)}')
	ans = list(crsr.fetchall()[0])
	crsr.execute(f'DELETE FROM STUDENTS WHERE id = {int(did)}')
	connection.commit()
	crsr.close()
	connection.close()
	return render_template('deleted.html',data=ans)

def setup_db():
	connection = sqlite3.connect("students.db")
	crsr = connection.cursor()
	crsr.execute("DROP TABLE IF EXISTS STUDENTS")
	crsr.execute("DROP TABLE IF EXISTS SCHOOL")
	crsr.execute("DROP TABLE IF EXISTS CLASS")
	tableA = """
		CREATE TABLE STUDENTS(
			first_name CHAR(32) NOT NULL,
			last_name CHAR(32) NOT NULL,
			major CHAR(32),
			gpa INTEGER,
			id CHAR(7) NOT NULL PRIMARY KEY
		);
	"""
	tableB = """
		CREATE TABLE SCHOOL(
			name CHAR(32) NOT NULL,
			number CHAR(7) NOT NULL PRIMARY KEY
		);
	"""
	tableC = """
		CREATE TABLE CLASS(
			capacity INTEGER,
			name CHAR(32) NOT NULL,
			number CHAR(7) NOT NULL PRIMARY KEY
		);
	"""
	crsr.execute(tableA)
	crsr.execute(tableB)
	crsr.execute(tableC)
	connection.commit()
	crsr.close()
	connection.close()

def main_data():
	connection = sqlite3.connect("students.db")
	crsr = connection.cursor()
	crsr.execute('INSERT INTO STUDENTS VALUES ("Luc", "Alexander", "CS", 4, "6758958");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Sam", "Situ", "CS", 3, "7589586");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Ian", "Demusis", "CS", 4, "5895867");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("John", "Doe", "Film", 2, "8958675");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Jane", "Dow", "Communications", 2, "9586758");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Lera", "Somova", "CS", 4, "5867589");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Roberto", "Laguna", "Music", 3, "8675895");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Maylo", "Domingo", "Architecture", 4, "1234567");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Pavlos", "Rosglou", "CS", 3, "7654321");')
	crsr.execute('INSERT INTO STUDENTS VALUES ("Ali", "Hachem", "Real Estate", 3, "0987654");')
	crsr.execute('INSERT INTO SCHOOL VALUES ("Suffolk University", "1234567");')
	crsr.execute('INSERT INTO CLASS VALUES (20, "Databases", "355");')
	connection.commit()
	crsr.close()
	connection.close()

def main():
	setup_db() # first time runs only
	main_data()
	app.run(debug=True)

if __name__=='__main__':
	main()
