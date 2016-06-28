from flask import Flask, session, redirect, render_template, request
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "sdghejrehwgafc"
mysql = MySQLConnector(app, "ajax_notes")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/update')
def update():
	query = "SELECT * FROM notes"
	notes = mysql.query_db(query)
	return render_template('partial.html', notes=notes)


@app.route('/new', methods=['POST'])
def new():
	query = "INSERT INTO notes (title, created_at) VALUES (:title, NOW())"
	data = {
		'title': request.form['title']
	}
	mysql.query_db(query, data)
	return redirect('/update')

@app.route('/desc/<id>', methods=['POST'])
def description(id):
	query = "UPDATE notes SET description = :description, updated_at = NOW() WHERE id = :id LIMIT 1"
	data = {
		'description': request.form['description'],
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/update')

@app.route('/delete/<id>')
def delete(id):
	query = "DELETE FROM notes WHERE id= :id LIMIT 1"
	data = {
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/update')

app.run(debug=True)
