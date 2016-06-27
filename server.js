from flask import Flask, session, redirect, render_template, request
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "sdghejrehwgafc"
mysql = MySQLConnector(app, "ajax")

@app.route('/')
def index():
	return render_template('index.html')









app.run(debug=True)
