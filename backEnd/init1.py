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

### Login Operations ###
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
	logname = request.form['logname'] # the logname means email (for customer, agent) or username (for airline staff)
	password = request.form['password']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	if (str(usertype) == "customer"):
		# customer uses email to log in
		query = 'SELECT * FROM customer WHERE email = %s and password = MD5(%s)'
	elif (str(usertype) == "airline_staff"):
		# airline staff uses username to log in
		query = 'SELECT * FROM airline_staff WHERE username = %s and password = MD5(%s)'
	elif (str(usertype) == "booking_agent"):
		# booking agent uses email to log in
		query = 'SELECT * FROM booking_agent WHERE email = %s and password = MD5(%s)'
	else:
		error = 'Invalid usertype, please identify your usertype'
		return render_template('login.html', error=error)
	cursor.execute(query, (logname, password))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if (data):
		session['logname'] = logname
		session['usertype'] = usertype
		return redirect(url_for('home'))
	else:
		# returns an error message to the html page
		error = 'Invalid username or password'
		return render_template('login.html', error=error)

### Register Operations ###
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
	cursor = conn.cursor()
	query_1 = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query_1, (username))
	# stores the results in a variable
	data_1 = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	# executes query
	query_2 = 'SELECT * FROM airline WHERE airline_name = %s'
	cursor.execute(query_2, (airline_name))
	data_2 = cursor.fetchone()
	error = None
	if (data_1):
		# If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	elif (not data_2):
		error = "No such airline"
		return render_template('register.html', error=error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, MD5(%s), %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/home')
def home():
	logname = session['logname']
	usertype = session['usertype']

	# get the customer's information and enter the customer's home page
	if (usertype == "customer"):
		app.logger.info("Customer: %s", logname)
		cursor = conn.cursor()
		query = 'SELECT * FROM customer WHERE email = %s'
		cursor.execute(query, (logname))
		customer_data = cursor.fetchone()
		cursor.close()
		customer_name = customer_data["name"]
		return render_template('home_customer.html', name=customer_name, data=customer_data)
	# get the airline staff's information and enter the airlie staff's home page
	elif (usertype == "airline_staff"):
		app.logger.info("Airline staff: %s", logname)
		cursor = conn.cursor()
		query = 'SELECT first_name, last_name FROM airline_staff WHERE username = %s'
		cursor.execute(query, (logname))
		airline_staff_data = cursor.fetchone()
		cursor.close()
		staff_name = airline_staff_data["first_name"] + " " + airline_staff_data["last_name"]
		return render_template('home_airline_staff.html', name=staff_name)
	# get the booking agent's information and enter the booking agent's home page
	elif (usertype == "booking_agent"):
		app.logger.info("Booking agent: %s", logname)
		return render_template('home_booking_agent.html', name=logname)
	else:
		return redirect('/')

### Airline Staff Functions ###

# a helper function to check the staff's permission
def check_permission(perm_to_check):
	# the perm_to_check is either 'admin' or 'operator'
	username = session['logname']
	cursor = conn.cursor()
	query = 'SELECT username, permission_type FROM permission WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchall()
	cursor.close()
	assert 0 <= len(data) <= 2
	# check in the fetched data: does the user have the permission that we want to check?
	if (len(data) == 2) and (data[0]["permission_type"] == perm_to_check or data[1]["permission_type"] == perm_to_check):
		return True
	elif (len(data) == 1) and (data[0]["permission_type"] == perm_to_check):
		return True
	else:
		return False

# view my flights
@app.route("/home/airline_staff_view_my_flights")
def airline_staff_view_my_flights():
	# Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days. 
	# He/she will be able to see all the current/future/past flights operated by the airline he/she works for based on range of dates, 
	# source/destination airports/city etc. 
	# He/she will be able to see all the customers of a particular flight.
	username = session['logname']
	cursor = conn.cursor()

	cursor.close()
	pass

# create new flights: for admin staff
@app.route("/home/airline_staff_create_new_flight", methods=['GET', 'POST'])
def airline_staff_create_new_flight():
	pass

# change flight status: for operator staff
@app.route("/home/airline_staff_change_flight_status")
def airline_staff_change_flight_status():
	pass

# add airplane: for admin staff
@app.route("/home/airline_staff_add_airplane", methods=['GET', 'POST'])
def airline_staff_add_airplane():
	pass

# add airport: for admin staff
@app.route("/home/airline_staff_add_airport", methods=['GET', 'POST'])
def airline_staff_add_airport():
	pass

### Logout Operation ###
@app.route('/logout')
def logout():
	session.pop('logname')
	session.pop('usertype')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
