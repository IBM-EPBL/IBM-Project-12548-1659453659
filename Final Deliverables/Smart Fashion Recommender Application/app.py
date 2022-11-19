from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=xhx40038;PWD=BDz5ow7439yj5PEd",'','')
print ("Database connection established", conn)

app = Flask(__name__)


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/addstudent')
def new_student():
    
    message = Mail(from_email="nithishjaganathanpersonal@gmail.com",to_emails="nithishjaganathan@gmail.com",subject="Account Registered Successfully",html_content="<p>Your account has been created using you provided email address.</p>")

    try:
     sg = SendGridAPIClient("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")
     response = sg.send(message)

    except Exception as e:
     print(e)
    return render_template('add_student.html')
  
@app.route('/loginpage')
def loginpage():
  return render_template('loginpage.html')

@app.route('/hpage')
def hpage():
  return render_template('hpage.html')

@app.route('/result')
def result():
  return render_template('result.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
   

    sql = "SELECT * FROM userdata WHERE name=? "
    stmt = ibm_db.prepare(conn, sql)  
    ibm_db.bind_param(stmt,1,name)   
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('loginpage.html', msg="please login using your details")
    else:
      insert_sql = "INSERT INTO userdata VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      
      ibm_db.execute(prep_stmt)
    
   
  return render_template('index.html', msg="Registered successfully")



@app.route('/check',methods = ['POST', 'GET'])
def check():
    
   if request.method == 'POST':
    
    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM userdata WHERE email=? and password= ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      return render_template('result.html', msg="SUCCESSFULLY LOGIN")
    else:
      return render_template('loginpage.html', msg="Please check your credentials!") 

  
  




  
  # # while student != False:
  # #   print ("The Name is : ",  student)

  # print(student)
 

# @app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# def edit(id):
    
#     post = BlogPost.query.get_or_404(id)

#     if request.method == 'POST':
#         post.title = request.form['title']
#         post.author = request.form['author']
#         post.content = request.form['content']
#         db.session.commit()
#         return redirect('/posts')
#     else:
#         return render_template('edit.html', post=post)