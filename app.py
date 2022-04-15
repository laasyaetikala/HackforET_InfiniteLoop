from email.headerregistry import Address
from logging import error
from msilib.schema import File
from pydoc import Doc
from tkinter import PhotoImage
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request

from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, FileField,SelectField,validators
from passlib.hash import sha256_crypt
from functools import wraps



app=Flask(__name__)

#config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='hostel_booking'
app.config['MYSQL_CURSORCLASS']='DictCursor'

#init MySQL
mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


class bookingForm(Form):
    name=StringField('Name',[validators.Length(min=1)])
    rollno=StringField('Roll No',[validators.Length(min=10,max=10)])
    branch=StringField('Branch',[validators.Length(min=1)])
    year=StringField('Year',[validators.Length(min=1)])
    hostel=StringField('Hostel',[validators.Length(min=1)])
    roomtype=StringField('Room Type',[validators.Length(min=1)])
    laundry=StringField('Laundry',[validators.Length(min=1)])
    mess=StringField('Mess',[validators.Length(min=1)])
    phoneno=StringField('Items',[validators.Length(min=10,max=10)])
    address=StringField('Address',[validators.Length(min=1,max=70)])
    city=StringField('City',[validators.Length(max=15)])
    pincode=StringField('Pincode',[validators.Length(max=6)])
    preferences=StringField('Preferences',[validators.Length(min=1)])

@app.route('/booking',methods=['GET','POST'])
def booking():
    form=bookingForm(request.form)
    if request.method=='POST':
        name=request.form['name']
        rollno=request.form['rollno']
        branch=request.form['branch']
        year=request.form['year']
        hostel=request.form['hostel']
        roomtype=request.form['roomtype']
        laundry=request.form['laundry']
        mess=request.form['mess']
        address=request.form['address']
        city=request.form['city']
        pincode=request.form['pincode']
        phoneno=request.form['phoneno']
        preferences=request.form['preferences']
        cur=mysql.connection.cursor()
        r=cur.execute("INSERT INTO booking(name,rollno,branch,year,hostel,roomtype,laundry,mess,phoneno,address,city,pincode,preferences) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,rollno,branch,year,hostel,roomtype,laundry,mess,phoneno,address,city,pincode,preferences))
        print(r)
        mysql.connection.commit()
        #close connection 
        cur.close()
        flash('Details Submitted!')
        return redirect('/booking')
    return render_template('booking.html',form=form)

class teambookingForm(Form):
    rollno_1=StringField('RollNo_1',[validators.Length(min=1)])
    rollno_2=StringField('RollNo_2',[validators.Length(min=1)])
    rollno_3=StringField('RollNo_3',[validators.Length(min=1)])
    rollno_4=StringField('RollNo_4',[validators.Length(min=1)])

@app.route('/teambooking',methods=['GET','POST'])
def teambooking():
    form=bookingForm(request.form)
    if request.method=='POST':
        rollno_1=request.form['rollno_1']
        rollno_2=request.form['rollno_2']
        rollno_3=request.form['rollno_3']
        rollno_4=request.form['rollno_4']
        cur=mysql.connection.cursor()
        r=cur.execute("INSERT INTO teambooking(rollno_1,rollno_2,rollno_3,rollno_4) VALUES(%s,%s,%s,%s)",(rollno_1,rollno_2,rollno_3,rollno_4))
        print(r)
        mysql.connection.commit()
        #close connection 
        cur.close()
        flash('Details Submitted!')
        return redirect('/teambooking')
    return render_template('teambooking.html',form=form)

@app.route('/hostel1')
def hostel1():
    return render_template('hostel1.html')

@app.route('/hostel2')
def hostel2():
    return render_template('hostel2.html')

@app.route('/hostel3')
def hostel3():
    return render_template('hostel3.html')
    
@app.route('/studentlogin')
def studentlogin():
    return render_template('studentlogin.html')

@app.route('/admin')
def admin():
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT * FROM booking")
    list=cur.fetchall()
    if result > 0:
        return render_template('admin.html',list=list)
    else:
        msg='No Items Found'
        return render_template('admin.html',msg=msg)
    cur.close()


@app.route('/biogasloc')
def biogasloc():
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT * FROM biogas")
    list=cur.fetchall()
    if result > 0:
        return render_template('biogasloc.html',list=list)
    else:
        msg='No Items Found'
        return render_template('biogasloc.html',msg=msg)
    cur.close()

@app.route('/about')
def about():
    return render_template('about.html')

class Register(Form):
    username=StringField('Username',[validators.Length(min=5)])
    password=PasswordField('Password',[validators.Length(min=5)])
#user registration
@app.route('/register',methods=['GET','POST'])
def register():
    print(request.method,'register def')
    form=Register(request.form)
    if request.method=='POST':
        print('hello')
        username=request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password'])) 
        print(username,' ',password)
        cur=mysql.connection.cursor()
        r=cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)",(username,password))
        print(r)
        mysql.connection.commit()
        #result=cur.execute("SELECT * FROM users WHERE username=%s",[username])
        cur.close()
        return redirect(url_for('home'))
    return render_template('register.html',form=form)

    
class Login(Form):
    username=StringField('Username',[validators.Length(min=5)])
    password=PasswordField('Password',[validators.Length(min=5)])
#user login
@app.route('/login',methods=['POST','GET'])
def login():    
    #form=Login(request.form)
    if request.method=='POST':
        username=request.form['username']
        password_candidate=request.form['password'] 
        cur=mysql.connection.cursor()
        result=cur.execute("SELECT * FROM users WHERE username=%s",[username])
        if result>0:
            #get stored hash
            data=cur.fetchone()
            password=data['password']
          
            #compare passwords
            if sha256_crypt.verify(password_candidate,password):
                #passed
                session['logged_in']=True
                session['username']=username
                # app.logger.info('PASSWORD MATCHED ')
                print('registered')
                return redirect(url_for('home'))
            else:
                error="invalid Login"
                # app.logger.info('PASSWORD NOT MATCHED')
                # flash('Invalid login','danger')
                return render_template('login.html',error=error)
        else:
            app.logger.info('no user')   
            error="username not found"
            return render_template('login.html',error=error)
    return render_template('login.html')
    



def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            #flash('Unauthorized, Please login','danger')
            return redirect(url_for('login')) 
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))


@app.route('/home')
@is_logged_in
def home():
    return render_template('home.html')


if __name__=='__main__':
    app.secret_key='raja'
    app.run(debug=True)