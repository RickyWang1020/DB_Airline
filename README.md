# DB_Airline

## About

This is a web-based Airline Ticket Reservation System developed using Python Flask, HTML and PHPMyAdmin. It is developed and tested on the MacOS System.

Team members: Yunhao Ye (yy2572@nyu.edu) and Xinran Wang (xw1744@nyu.edu).

It serves as the Final Project for Databases course Spring 2022, NYU Shanghai.

## Requirements

- Xampp 7.4.27
- Python Flask, pyMySql modules

## How to Use

1. Launch Xampp, start the Apache server
2. Run `backEnd/init1.py`
3. On web browser, type `http://127.0.0.1:5000` to interact with the webpage

## Folder Structure

- README.md: this documentation file
- backEnd: the folder containing backend information such as database management and system design
  - *create_system_tables.sql*: sql file for creating tables in the database
  - *init1.py*: the main file for launching the backend of the airline ticket system
  - *load_data_demo.sql*: sql file for loading test data in the database
  - *use_case_query.md*: the file that lists all the use cases and the SQL queries executed by them
- frontEnd: the folder containing all frontend rendering of the system, each file corresponds to the functionality as its filename suggests
  - *airline_staff_add_airplane.html*: html file for Airline Staff feature 4
  - *airline_staff_add_airport.html*: html file for Airline Staff feature 5
  - *airline_staff_add_booking_agent.html*: html file for Airline Staff feature 12
  - *airline_staff_change_flight_status.html*: html file for Airline Staff feature 3
  - *airline_staff_compare_revenue.html*: html file for Airline Staff feature 9
  - *airline_staff_create_new_flight.html*: html file for Airline Staff feature 2
  - *airline_staff_grant_new_permission.html*: html file for Airline Staff feature 11
  - *airline_staff_view_booking_agent.html*: html file for Airline Staff feature 6
  - *airline_staff_view_frequent_customer.html*: html file for Airline Staff feature 7
  - *airline_staff_view_my_flights.html*: html file for Airline Staff feature 1
  - *airline_staff_view_reports.html*: html file for Airline Staff feature 8
  - *airline_staff_view_top_destination.html*: html file for Airline Staff feature 10
  - *booking_agent_search_for_flights.html*: html file for Booking Agent feature 2 and 3
  - *booking_agent_view_my_commission.html*: html file for Booking Agent feature 4
  - *booking_agent_view_my_flights.html*: html file for Booking Agent feature 1
  - *booking_agent_view_top_customers.html*: html file for Booking Agent feature 5
  - *customer_search_for_flights.html*: html file for Customer feature 2 and 3
  - *customer_track_my_spending.html*: html file for Customer feature 4
  - *customer_view_my_flights.html*: html file for Customer feature 1
  - *home_airline_staff.html*: html file for the homepage of Airline Staff, which includes buttons directing to Airline Staff's use cases
  - *home_booking_agent.html*: html file for the homepage of Booking Agent, which includes buttons directing to Booking Agent's use cases
  - *home_customer.html*: html file for the homepage of Customer, which includes buttons directing to Customer's use cases
  - *index.html*: html file for the welcome page of public info
  - *login.html*: html file for the login page
  - *register.html*: html file the registration page, where the user selects which user-type they want to register as
  - *register_airline_staff.html*: html file for registering as an Airline Staff
  - *register_booking_agent.html*: html file for registering as a Booking Agent
  - *register_customer.html*: html file for registering as a Customer

## Summary of Teamwork

- Yunhao Ye is responsible for the Backend and Frontend developments of: 
  - 3 types of user Registration
  - Customer and Booking Agent features

- Xinran Wang is responsible for the Backend and Frontend developments of: 
  - 3 types of user Login, and the public info page
  - Airline Staff features

- We collaborated with each other to divide the tasks and carry out the system testing

<img width="917" alt="teamwork_summary" src="https://user-images.githubusercontent.com/50431019/168847343-015672ab-b0fc-4557-b47a-2fd683591466.png">
