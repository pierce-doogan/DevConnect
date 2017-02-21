from __future__ import print_function
import sys
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jeff'
app.config['MYSQL_DATABASE_PASSWORD'] = 'superduperpasswordtest'
app.config['MYSQL_DATABASE_DB'] = 'students'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _first_name = request.form['inputFirstName']
        _last_name = request.form['inputLastName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _first_name and _last_name and _email and _password:
            print('We got the fields', file=sys.stderr)
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('createUser',(_first_name,_last_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        print('Exception thrown', file=sys.stderr)
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(port=5000)