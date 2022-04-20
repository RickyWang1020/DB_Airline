# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import logging


# Initialize the app from Flask
app = Flask(__name__, template_folder='../frontEnd')

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

# Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	# grabs information from the forms
	usertype = request.form.get('usertype')
	app.logger.info(usertype)
	username = request.form['username']
	password = request.form['password']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	if (str(usertype) == "customer"):
		query = 'SELECT * FROM customer WHERE name = %s and password = MD5(%s)'
	elif (str(usertype) == "airline_staff"):
		query = 'SELECT * FROM airline_staff WHERE name = %s and password = MD5(%s)'
	elif (str(usertype) == "booking_agent"):
		query = 'SELECT * FROM booking_agent WHERE name = %s and password = MD5(%s)'
	else:
		error = 'Invalid usertype, please identify your usertype'
		return render_template('login.html', error=error)
	cursor.execute(query, (username, password))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if (data):
		session['username'] = username
		session['usertype'] = usertype
		return redirect(url_for('home'))
	else:
		# returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

# Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/registerCustomer')
def registerCustomer():
	return render_template('register_customer.html')

@app.route('/registerBookingAgent')
def registerBookingAgent():
	return render_template('register_booking_agent.html')

@app.route('/registerAirlineStaff')
def registerAirlineStaff():
	return render_template('register_airline_staff.html')

# Authenticates the register for customer
@app.route('/registerCustomerAuth', methods=['GET', 'POST'])
def registerCustomerAuth():
	# grabs information from the forms
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']
	# app.logger.info(role)
	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	error = None
	if (data):
		# If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the register for booking agent
@app.route('/registerBookingAgentAuth', methods=['GET', 'POST'])
def registerBookingAgentAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']
	# app.logger.info(role)
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if (data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, MD5(%s), %s)'
		cursor.execute(ins, (email, password, booking_agent_id))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the register for airline staff
@app.route('/registerAirlineStaffAuth', methods=['GET', 'POST'])
def registerAirlineStaffAuth():
	# grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']
	# app.logger.info(role)
	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query_1 = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	# stores the results in a variable
	data_1 = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	# executes query
	query_2 = 'SELECT * FROM airline WHERE airline_name = %s'
	cursor.execute(query, (airline_name))
	# stores the results in a variable
	data_2 = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	error = None
	if (data1):
		# If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	elif (not data2):
		error = "No such airline"
		return render_template('register.html', error=error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/viewMyFlights', methods=['GET', 'POST'])
def registerCustomerAuth():
	# grabs information from the forms
	username = session['username']
	usertype = session['usertype']
	query_1 = 'SELECT * FROM flight WHERE where (airline_name, flight_num) in %s ORDER BY departure_time'
	if (usertype == "customer"):
		app.logger.info(username)
		cursor = conn.cursor()
		query_2 = 'SELECT airline_name, flight_num FROM ticket, purchase WHERE customer_email = %s'
		cursor.execute(query_2, (username))
		data2 = cursor.fetchone()
		cursor.execute(query_1, (data2))
		data1 = cursor.fetchone()
		cursor.close()
		return render_template('view_flights_customer.html', username=username, flights_result=data1)
	if (usertype == "booking_agent"):
		app.logger.info(username)
		cursor = conn.cursor()
		query_2 = 'SELECT airline_name, flight_num FROM ticket, purchase WHERE booking_agent_id = %s'
		cursor.execute(query_2, (username))
		data2 = cursor.fetchone()
		cursor.execute(query_1, (data2))
		data1 = cursor.fetchone()
		cursor.close()
		return render_template('view_flights_customer.html', username=username, flights_result=data1)
	if (usertype == "airline_staff"):
		app.logger.info(username)
		cursor = conn.cursor()
		query_2 = 'SELECT airline_name FROM airline_staff WHERE username = %s'
		cursor.execute(query_2, (username))
		data2 = cursor.fetchone()
		query_3 = 'SELECT * FROM flight WHERE where airline_name = %s ORDER BY departure_time'
		cursor.execute(query_1, (data2))
		data1 = cursor.fetchone()
		cursor.close()
		return render_template('view_flights_customer.html', username=username, flights_result=data1)

@app.route('/home')
def home():
	username = session['username']
	usertype = session['usertype']

	if (usertype == "customer"):
		app.logger.info(username)
		cursor = conn.cursor()
		query = 'SELECT name, email FROM customer WHERE name = %s'
		cursor.execute(query, (username))
		data1 = cursor.fetchone()
		cursor.close()
		return render_template('home.html', username=username, posts=data1)
	elif (usertype == "airline_staff"):
		app.logger.info(username)
		cursor = conn.cursor()
		query = 'SELECT name, email FROM airline_staff WHERE name = %s'
		cursor.execute(query, (username))
		data1 = cursor.fetchone()
		cursor.close()
		return render_template('home.html', username=username, posts=data1)
	elif (usertype == "booking_agent"):
		app.logger.info(username)
		cursor = conn.cursor()
		query = 'SELECT name, email FROM booking_agent WHERE name = %s'
		cursor.execute(query, (username))
		data1 = cursor.fetchone()
		cursor.close()
		return render_template('home.html', username=username, posts=data1)

    # cursor = conn.cursor();
    # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    # cursor.execute(query, (username))
    # data1 = cursor.fetchall() 
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
    # return render_template('home.html', username=username, posts=data1)

@app.route('/customerHome')
def customer_home():
	username = session['username']
	cursor = conn.cursor()
	query = 'SELECT name, email FROM customer WHERE name = %s'
	cursor.execute(query, (username))
	data1 = cursor.fetchone() 
	app.logger.info(data1)
	print(data1['name'], data1['email'])
	cursor.close()
	return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	session.pop('usertype')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
