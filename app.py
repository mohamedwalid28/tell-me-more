from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import uuid
from werkzeug.security import check_password_hash



app = Flask(__name__, template_folder='../Tell me more/template', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://WALIDSPC/tellmemore?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
app.secret_key = "my_super_secret_key_123"
db = SQLAlchemy(app)


class user(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': False}

    username = db.Column(db.String(50), nullable = False, primary_key=True)  #,default=lambda: str(uuid.uuid4())
    useremail = db.Column(db.String(50), nullable=False)
    userpass = db.Column(db.String(50), nullable=False)

def insertuser(name, email, password):
    inserteduser = [
        user(
            username = name,  
            useremail = email,
            userpass = password
        )
    ]
    db.session.add_all(inserteduser)
    db.session.commit()
    

@app.route('/')
@app.route('/index')
def index():
    return render_template('master_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Corrected to use 'user' instead of 'User'
        user_instance = user.query.filter_by(username=username, userpass=password).first()
        
        if user_instance:
            session['username'] = user_instance.username
            return redirect(url_for('success'))
        else:
            flash('Invalid username or password')
    
    return render_template('sign_in.html')


@app.route('/success')
def success():
    if 'username' in session:
        return render_template('ready_novels\'page.html', username = session['username'])
    else:
        return redirect(url_for('home'))
  
  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match", 400

        existing_user = user.query.filter_by(username=username).first()
        if existing_user is not None:
            return "Username already exists", 400

        new_user = user(username=username, useremail=email, userpass=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('sign_up.html')
        
@app.route('/logout')
def logout():
    session.clear
    return render_template("master_page.html")
        
if __name__ == '__main__':
    app.run(debug=True)
