from flask import Flask, render_template, request, redirect, url_for 
import psycopg2 

app = Flask(__name__) 


def DatabaseConnection():	
# Connect to the database 
    conn = psycopg2.connect(database="flask_db", user="postgres", 
						password="postgres", host="localhost", port="5432")
    return conn; 


conn=DatabaseConnection();
# create a cursor 
cur = conn.cursor() 

# if you already have any table or not id doesnt matter this 
# will create a users table for you. 
cur.execute( 
	'''CREATE TABLE IF NOT EXISTS users (id serial 
	PRIMARY KEY, name varchar(100), email varchar(100));''')  

# commit the changes 
conn.commit() 

# close the cursor and connection 
cur.close() 
conn.close() 


@app.route('/users') 
def index(): 
	conn=DatabaseConnection();

	cur = conn.cursor() 

	# Select all products from the table 
	cur.execute('''SELECT * FROM users''') 

	# Fetch the data 
	data = cur.fetchall() 

	cur.close() 
	conn.close() 

	return {'data':data}; 


@app.route('/users', methods=['POST']) 
def create(): 
	try:
		conn=DatabaseConnection();

		cur = conn.cursor() 
		data=request.get_json();
		name = data['name'];
		email = data['email'] 

		# Insert the data into the table 
	
		cur.execute( 
			'''INSERT INTO users 
			(name, email) VALUES (%s, %s)''', 
			(name, email));
		conn.commit()
		return {"status":200,"message":"User created successfully"}
	except Exception as e:
		return {"status":500,"message":"Failed to create user"}
	finally:
		cur.close() 
		conn.close() 


if __name__ == '__main__': 
	app.run(debug=True) 
