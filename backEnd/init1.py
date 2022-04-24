# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
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
		flash("Invalid usertype, please identify your usertype")
		return redirect(url_for("login"))
	cursor.execute(query, (logname, password))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	cursor.close()
	if (data):
		session['logname'] = logname
		session['usertype'] = usertype
		return redirect(url_for('home'))
	else:
		# returns an error message to the html page
		flash("Invalid username or password")
		return redirect(url_for("login"))

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
	if (data):
		# If the previous query returns data, then user exists
		flash("This user already exists")
		return render_template('register_customer.html')
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
	if (data):
		#If the previous query returns data, then user exists
		flash("This user already exists")
		return render_template('register_booking_agent.html')
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
	if (data_1):
		# If the previous query returns data, then user exists
		flash("This user already exists")
		return render_template('register_airline_staff.html')
	elif (not data_2):
		flash("No such airline")
		return render_template('register_airline_staff.html')
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
def check_permission(username, perm_to_check):
	# the perm_to_check is either 'admin' or 'operator'
	cursor = conn.cursor()
	query = 'SELECT username, permission_type FROM permission WHERE username = %s AND permission_type = %s'
	cursor.execute(query, (username, perm_to_check))
	data = cursor.fetchall()
	cursor.close()
	if (data):
		return True
	else:
		return False

# view my flights
@app.route("/home/airline_staff_view_my_flights", methods=['GET','POST'])
def airline_staff_view_my_flights():
	# Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days. 
	# He/she will be able to see all the current/future/past flights operated by the airline he/she works for based on range of dates, 
	# source/destination airports/city etc. 
	# He/she will be able to see all the customers of a particular flight.
	username = session['logname']
	cursor = conn.cursor()

	# get the airline name that the staff belongs to
	query_1 = "SELECT airline_name FROM airline_staff WHERE username = %s"
	cursor.execute(query_1, (username))
	airline_name = cursor.fetchone()
	app.logger.info("airline name is %s", airline_name)

	# default: get the upcoming flights of the airline for the next 30 days
	query_2 = "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price, status, airplane_id, GROUP_CONCAT(customer_email SEPARATOR ', ') as customers \
		FROM flight NATURAL LEFT OUTER JOIN (ticket NATURAL JOIN purchases) \
		WHERE airline_name = %s "
	time_range_statement = "AND (departure_time BETWEEN NOW() AND ADDTIME(NOW(), '30 0:0:0')) "

	# get source/destination airports/city, for customized selections
	query_3 = "SELECT DISTINCT f.departure_airport AS depart_airport, a.airport_city AS departure_city FROM flight f JOIN airport a ON (f.departure_airport = a.airport_name)"
	cursor.execute(query_3)
	departure_airport_city = cursor.fetchall()
	query_4 = "SELECT DISTINCT f.arrival_airport AS arr_airport, a.airport_city AS arrival_city FROM flight f JOIN airport a ON (f.arrival_airport = a.airport_name)"
	cursor.execute(query_4)
	arrival_airport_city = cursor.fetchall()
	app.logger.info("depart is %s, arrival is %s", departure_airport_city, arrival_airport_city)

	if request.method == "POST":
		# get from the form result: the range of dates that the staff wants to check
		start_date = request.form["range_start"]
		end_date = request.form["range_end"]
		
		# get from the form result: the departure and arrival city/ airport
		departure = []
		for i in range(len(departure_airport_city)):
			try:
				data = request.form["departure: "+str(i)]
				departure.append(departure_airport_city[i])
			except:
				pass
		arrival = []
		for j in range(len(arrival_airport_city)):
			try:
				data = request.form["arrival: "+str(j)]
				arrival.append(arrival_airport_city[j])
			except:
				pass
		app.logger.info("the submitted data is %s, %s, %s, %s", start_date, end_date, departure, arrival)

		# prepare the query for filtered search
		# the departure date range selection
		if start_date and end_date:
			time_range_statement = "AND DATE(departure_time) BETWEEN \'{}\' AND \'{}\' ".format(start_date, end_date)
		elif start_date:
			time_range_statement = "AND DATE(departure_time) >= \'{}\' ".format(start_date)
		elif end_date:
			time_range_statement = "AND DATE(departure_time) <= \'{}\' ".format(end_date)
		else:
			time_range_statement = " "
		
		# the departure/arrival airport selection
		if departure:
			departure_statement = ""
			for d in departure:
				departure_statement += "\'" + d["depart_airport"].replace("\'", "\\\'") + "\'" + ", "
			departure_statement = departure_statement.strip(", ")
			departure_statement = "(" + departure_statement + ") "
			app.logger.info("departure statement: %s", departure_statement)
			query_2 += "AND departure_airport IN " + departure_statement
		if arrival:
			arrival_statement = ""
			for a in arrival:
				arrival_statement += "\'" + a["arr_airport"].replace("\'", "\\\'") + "\'" + ", "
			arrival_statement = arrival_statement.strip(", ")
			arrival_statement = "(" + arrival_statement + ") "
			app.logger.info("arrival_statement statement: %s", arrival_statement)
			query_2 += "AND arrival_airport IN " + arrival_statement
				
	# now execute the flight search query to get the filtered (if applicable) search result
	query_2 += time_range_statement
	query_2 += "GROUP BY airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price, status, airplane_id\
		ORDER BY departure_time, arrival_time"
	app.logger.info("the query for flight is: %s", query_2)
	cursor.execute(query_2, (airline_name["airline_name"]))
	flights = cursor.fetchall()
	cursor.close()

	return render_template("airline_staff_view_my_flights.html", flights=flights, departure_airport_city=departure_airport_city, arrival_airport_city=arrival_airport_city)

# create new flights: for admin staff
@app.route("/home/airline_staff_create_new_flight", methods=['GET', 'POST'])
def airline_staff_create_new_flight():
	username = session['logname']
	is_admin = check_permission(username, 'admin')
	# if not admin, then refuse to do this
	if (not is_admin):
		flash("Unauthorized Operation: You do not have Admin Permission!")
		return redirect(url_for("home"))

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
