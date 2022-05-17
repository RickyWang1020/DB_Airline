# DB_Airline

## About

This is a web-based Airline Ticket Reservation System developed using Python Flask, HTML and PHPMyAdmin. It is developed and tested on the MacOS System.

Team members: Yunhao Ye (yy2572@nyu.edu) and Xinran Wang (xw1744@nyu.edu).

It serves as the Final Project for Databases course Spring 2022, NYU Shanghai.

## Requirements

- Xampp 7.4.27
- Python Flask, pyMySql modules

## Folder Structure

- README.md: this documentation file
- backEnd: the folder containing backend information such as database management and system design
  - *create_system_tables.sql*: sql file for creating tables in the database
  - *init1.py*: the main file for launching the backend of the airline ticket system
  - *load_data_demo.sql*: sql file for loading test data in the database
  - *use_case_query.md*: the file that lists all the use cases and the queries executed by them
- frontEnd: the folder containing all frontend rendering of the system, each file corresponds to the functionality as its filename suggests
  - *airline_staff_add_airplane.html*
  - *airline_staff_add_airport.html*
  - *airline_staff_add_booking_agent.html*
  - *airline_staff_change_flight_status.html*
  - *airline_staff_compare_revenue.html*
  - *airline_staff_create_new_flight.html*
  - *airline_staff_grant_new_permission.html*
  - *airline_staff_view_booking_agent.html*
  - *airline_staff_view_frequent_customer.html*
  - *airline_staff_view_my_flights.html*
  - *airline_staff_view_reports.html*
  - *airline_staff_view_top_destination.html*
  - *booking_agent_search_for_flights.html*
  - *booking_agent_view_my_commission.html*
  - *booking_agent_view_my_flights.html*
  - *booking_agent_view_top_customers.html*
  - *customer_search_for_flights.html*
  - *customer_track_my_spending.html*
  - *customer_view_my_flights.html*
  - *home_airline_staff.html*
  - *home_booking_agent.html*
  - *home_customer.html*
  - *index.html*: the welcome page of public info
  - *login.html*: the login page
  - *register.html*: the registration (sign up) page
  - *register_airline_staff.html*
  - *register_booking_agent.html*
  - *register_customer.html*

## Summary of Teamwork

- Yunhao Ye is responsible for the Backend and Frontend developments of: 
  - 3 types of user Registration
  - Customer and Booking Agent features

- Xinran Wang is responsible for the Backend and Frontend developments of: 
  - 3 types of user Login, and the public info page
  - Airline Staff features

- We collaborated with each other to divide the tasks and carry out the system testing

<img width="917" alt="teamwork_summary" src="https://user-images.githubusercontent.com/50431019/168847343-015672ab-b0fc-4557-b47a-2fd683591466.png">
