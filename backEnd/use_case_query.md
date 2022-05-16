# Use Cases and Queries

## Welcome Page

1. **View Public Info**: All users, whether logged in or not, can search for upcoming flights based on source city/airport name, destination city/airport name, date. The user will be able to see the flight's status based on flight number, arrival/departure date.

- The default query is to get the upcoming 30 day's flight information:

``` sql
SELECT * 
FROM flight 
WHERE True 
AND departure_time BETWEEN NOW() AND ADDTIME(NOW(), '30 0:0:0');
```

- If user specifies only part of the selections from "departure date start, departure date end, departure city and airport, and arrival city and airport" (i.e., vague search):

``` sql
SELECT *
FROM flight
WHERE True 
AND arrival_airport IN ('PVG', 'JFK')
AND DATE(departure_time) >= '2022-03-01' 
ORDER BY departure_time, arrival_time;
```

- If user specifies all the selections:

``` sql
SELECT *     
FROM flight 
WHERE True 
AND departure_airport IN ('La Guardia') 
AND arrival_airport IN ('Louisville SDF', 'PVG') 
AND DATE(departure_time) BETWEEN '2022-03-01' AND '2022-07-05' 
ORDER BY departure_time, arrival_time;
```

2. **Register**: 3 types of user registrations (Customer, Booking agent, Airline staff) option via forms.

- Customer:

``` sql
INSERT INTO customer 
VALUES('test_email', 'test_name', MD5('pwd'), 123, 'test_street', 'ny', 'ny', 12345678, 'Passport123', '2025-05-01', 'China', '1980-01-01');
```

- Booking Agent:

``` sql
INSERT INTO booking_agent 
VALUES('test_email', MD5('pwd'), 111);
```

- Airline Staff:

``` sql
INSERT INTO airline_staff 
VALUES('test_username', MD5('pwd'), 'firstname', 'lastname', '1980-01-01', 'Jet Blue');
```

3. **Login**: 3 types of user login (Customer, Booking agent, Airline Staff). User enters their username (email address will be used as username), x, and password, y, via forms on login page. This data is sent as POST parameters to the login-authentication component, which checks whether there is a tuple in the Person table with username=x and the password = md5(y).

- Customer:

``` sql
SELECT * 
FROM customer 
WHERE email = 'test_email' AND password = MD5('pwd');
```

- Booking Agent:

``` sql
SELECT * 
FROM booking_agent 
WHERE email = 'test_email' AND password = MD5('pwd');
```

- Airline Staff:

``` sql
SELECT * 
FROM airline_staff 
WHERE username = 'test_username' AND password = MD5('pwd');
```

## Customer

1. **View My flights**: Provide various ways for the user to see flights information which he/she purchased. The default should be showing for the upcoming flights. The user can vaguely specify a range of dates, specify destination and/or source airport name or city name.
2. **Purchase tickets**: Customer chooses a flight and purchase ticket for this flight.
3. **Search for flights**: Search for upcoming flights based on source city/airport name, destination city/airport name, date.
4. **Track My Spending**: Default view will be total amount of money spent in the past year and a bar chart showing month wise money spent for last 6 months. He/she will also have option to specify a range of dates to view total amount of money spent within that range and a bar chart showing month wise money spent within that range.

## Booking Agent

1. **View My flights**: Provide various ways for the booking agents to see flights information for which he/she purchased on behalf of customers. The default should be showing for the upcoming flights. The user can specify a range of dates, specify destination and/or source airport name and/or city name etc to show all the flights for which he/she purchased tickets.
2. **Purchase tickets**: Booking agent chooses a flight and purchases tickets for other customers giving customer information. The booking agent may only purchase tickets from airlines they work for.
3. **Search for flights**: Search for upcoming flights based on source city/airport name, destination city/airport name, date.
4. **View my commission**: Default view will be total amount of commission received in the past 30 days and the average commission he/she received per ticket booked in the past 30 days and total number of tickets sold by him in the past 30 days. He/she will also have option to specify a range of dates to view total amount of commission received and total numbers of tickets sold.
5. **View Top Customers**: Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and top 5 customers based on amount of commission received in the last year. Show a bar chart showing each of these 5 customers in x-axis and number of tickets bought in y-axis. Show another bar chart showing each of these 5 customers in x-axis and amount commission received in y- axis.

## Airline Staff

1. **View My flights**: Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based on range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.
2. **Create new flights**: He or she creates a new flight, providing all the needed data, via forms. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days.
3. **Change Status of flights**: He or she changes a flight status (from upcoming to in progress, in progress to delayed etc) via forms. The application should prevent unauthorized users or staffs without "Operator" permission from doing this action.
4. **Add airplane in the system**: He or she adds a new airplane, providing all the needed data, via forms. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. In the confirmation page, she/he will be able to see all the airplanes owned by the airline he/she works for.
5. **Add new airport in the system**: He or she adds a new airport, providing all the needed data, via forms. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action.
6. **View all the booking agents**: Top 5 booking agents based on number of tickets sales for the past month and past year. Top 5 booking agents based on the amount of commission received for the last year.
7. **View frequent customers**: Airline Staff will also be able to see the most frequent customer within the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.
8. **View reports**: Total amounts of ticket sold based on range of dates/last year/last month etc. Month-wise tickets sold in a bar chart.
9. **Comparison of Revenue earned**: Draw a pie chart for showing total amount of revenue earned from direct sales (when customer bought tickets without using a booking agent) and total amount of revenue earned from indirect sales (when customer bought tickets using booking agents) in the last month and last year.
10. **View Top destinations**: Find the top 3 most popular destinations for last 3 months and last year.
11. **Grant new permissions**: Grant new permissions to other staffs in the same airline. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. Initially there should be a staff with "Admin" permission in the database for each airline. Airline staffs registered through the application DO NOT have any permissions at beginning.
12. **Add booking agents**: Add booking agents that can work for this airline, providing their email address. The application should prevent unauthorized users or staffs without "Admin" permission from doing this action. A booking agent cannot work for any airline (thus cannot purchase tickets) until any staff add them through this action.
