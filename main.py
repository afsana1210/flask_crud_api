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

	

@app.route('/update/<int:user_id>', methods=['PUT']) 
def update(user_id): 

    try:
        conn=DatabaseConnection()
        cur=conn.cursor()
        data=request.get_json();
        cur.execute('''SELECT * FROM users WHERE id=%s''',(user_id,)) 
        id= cur.fetchone()[0]
        name=data['name']
        email=data['email']

        if id == user_id:
            cur.execute( 
					'''UPDATE users SET name=%s,
					email=%s WHERE id=%s''', (name, email, user_id)) 

            conn.commit() 
            return{"status":200,"message":"Data updated succesfully","data":data}
        else:
          return{"status":404,"message":"User not found"}
    except Exception as e:
       return{"status":500,"message":"Failed to update data"}
    finally:
      cur.close()
      conn.close()


@app.route('/delete/<int:user_id>', methods=['DELETE']) 
def delete(user_id): 
	try:
		conn=DatabaseConnection();
		cur = conn.cursor() 
		
		cur.execute('''SELECT * FROM users WHERE id=%s''',(user_id,)) 
		id= cur.fetchone()[0]
	
		if user_id == id:

		    # Delete the data from the table 
			cur.execute('''DELETE FROM users WHERE id=%s''', (id,))
			conn.commit()
			return {"status":200,"message":"Record deleted sucessfully"}
		else:
			return {"status":404 , "message":"User Not found"}
	except Exception as e:
            return {"status":500 , "message":"Failed to delete record"}
          



if __name__ == '__main__': 
	app.run(debug=True) 
