# essenvia_assignment_1



#Tech Stack:
Backend : Django
Database : PostgreSql

1) How to set-up the database:

a) install postgreSql
	https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

b) Set:
	username = postgres
	password = 123
	database = postgres

2) git clone https://github.com/yogeshTheCaptain/essenvia_assignment_1.git

3) electronic_store/order_management/Database/ :
	Run data_table.py

	It will create table in the database

4) Put some dummy data in warehouse inventory table

5) Put two rows in team_table and just put data in team column in first row as 'A' and in second as 'B'

5) Run python3 manage.py runserver

6) APi Call to check Inventory Status: (It will provide all the available inventory only)

	curl -X GET \
	  http://127.0.0.1:8000/inventory/ \
	  -H 'Postman-Token: 5ebfa8c3-3978-4156-8bfd-daf99e7df1da' \
	  -H 'cache-control: no-cache'

7) Api Call to check Order Status and Order Number: (If one of the Item is available then the order will be placed)
	curl -X POST \
	  http://127.0.0.1:8000/placeOrder/ \
	  -H 'Content-Type: application/json' \
	  -H 'Postman-Token: 3d916814-a26c-4b7a-b75d-565bb6ec629f' \
	  -H 'cache-control: no-cache' \
	  -d '{
	  "customer_name": "Yogesh",
	  "address": "Vijaypark",
	  "distance": 4,
	  "items": [{"item":"T2020UHD","quantity":1,"price":"20000"},{"item":"R260LCS","quantity":1,"price":"20000"}]
	  

	}'

8) Fetch current day orders details: (It will provide the current day orders status)
	curl -X GET \
	http://127.0.0.1:8000/orders/ \
	-H 'Postman-Token: 2e8c66c8-5b02-4de7-9092-5cda99157e94' \
	-H 'cache-control: no-cache'



