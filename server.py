from flask import Flask, session, redirect, render_template, request
from mysqlconnection import MySQLConnector
import math

app = Flask(__name__)
app.secret_key = "sdghejrehwgafc"
mysql = MySQLConnector(app, "ajax_notes")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/update')
def update():
	query = "SELECT * FROM notes LIMIT 5"
	notes = mysql.query_db(query)
	return render_template('partial.html', notes=notes, pages = [1])

@app.route('/update/<page>')
def updatepage(page):
	arr = []
	pages = []
	for page in range(0,int(page)):
		arr.append(page)
		print arr, "ARR"
	query = "SELECT * FROM notes LIMIT :page, :pagelimit"
	data = {
		'page': int(page) * 5,
		'pagelimit': 5
	}
	notes = mysql.query_db(query, data)
	countquery = "SELECT COUNT(title) FROM notes"
	count = mysql.query_db(countquery)
	count = count[0]['COUNT(title)']
	pages = int(math.ceil(count / 5))
	for num in xrange(0, pages + 1):
		arr.append(num + 1)
		print num, arr, "tewasgec"
	return render_template('partial.html', notes=notes, pages=arr)

@app.route('/new', methods=['POST'])
def new():
	query = "INSERT INTO notes (title, created_at) VALUES (:title, NOW())"
	data = {
		'title': request.form['title']
	}
	mysql.query_db(query, data)
	return redirect('/update/1')

@app.route('/desc/<id>', methods=['POST'])
def description(id):
	query = "UPDATE notes SET description = :description, updated_at = NOW() WHERE id = :id LIMIT 1"
	data = {
		'description': request.form['description'],
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/update/1')

@app.route('/delete/<id>')
def delete(id):
	query = "DELETE FROM notes WHERE id= :id LIMIT 1"
	data = {
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/update/1')

app.run(debug=True)
