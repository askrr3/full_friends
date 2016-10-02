from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)

mysql = MySQLConnector(app,'friendsdb')
app.secret_key = "ThisIsSecret!"

@app.route('/')
def index():
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	return render_template('index.html', all_friends=friends)

@app.route('/friends', methods=['POST'])
def create():
	first = request.form['first_name']
	last = request.form['last_name']

	query = 'INSERT INTO friends (first_name, last_name, created_at) VALUES (:first_name, :last_name, NOW())'
	data = {
			'first_name': first,
			'last_name': last
			}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/friends/<id>/edit', methods=['POST'])
def edit(id):
	query = "SELECT * FROM friends WHERE id =" + id
	
	friend = mysql.query_db(query)

	print friend
	return render_template('edit.html',id = id, friend = friend)


@app.route('/friends/<id>', methods=['POST'])
def update(id):

	first = request.form['first_name']
	last = request.form['last_name']

	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name WHERE id = :id"
	data = {
			'id' : id,
			'first_name': first,
			'last_name': last			
			}
	mysql.query_db(query, data)
	return redirect('/')
	# return render_template('edit.html', id=id)


@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
	query = "DELETE FROM friends WHERE id = :id"
	data = {'id': id}
	mysql.query_db(query, data)
	return redirect('/')

app.run(debug=True)




