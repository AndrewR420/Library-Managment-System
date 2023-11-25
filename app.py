from flask import Flask, render_template, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Setup app to use SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

# load book data
df = pd.read_csv("static/books2.csv",sep=";", encoding='latin-1')

# setup databse for books
class BookModel(db.Model):
    title = db.Column(db.String(100),unique=False)
    author = db.Column(db.String(100),unique=False)
    isbn = db.Column(db.Integer(),primary_key=True)

    def __repr__(self):
        return f"Book:{self.title},{self.author},ISBN:{self.isbn}"

# setup database for to store users
class User(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

# setup database that stores books checkedout by users
class Checkout(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    user_email = db.Column(db.String(100),db.ForeignKey('user.email'))
    isbn = db.Column(db.Integer(),db.ForeignKey('book_model.isbn'))
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Checkout:{self.user_email} - {self.isbn}"

# Create tables in Database
with app.app_context():
    db.create_all()
    # creating admin user
    admin_email = "admin@gmail.com"
    admin_password = generate_password_hash("super_secret_password")
    admin_user = User(email=admin_email,password=admin_password, is_admin=True)

     # Check if an admin user already exists to avoid duplicates
    existing_admin = User.query.get(admin_email)
    if not existing_admin:
        db.session.add(admin_user)
        db.session.commit()

    # Load book data from CSV and add to database
    for _, row in df.iterrows(): 
        try:
            book = BookModel(title=row['Book-Title'], author=row['Book-Author'], isbn=int(row['ISBN']))
            db.session.merge(book)
            db.session.commit()
        except:
            pass

# homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# create user page
@app.route('/create_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        member = User.query.get(email)
        if member == None: # if member doesnt exist hash password and add user to database
            hashed_password = generate_password_hash(password)
            new_member = User(email=email,password=hashed_password)
            db.session.add(new_member)
            db.session.commit()
        redirect('/')
    
    return render_template('create_user.html')

 # login page and hashing password    
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.get(email)

        if user and check_password_hash(user.password, password):
            if user.is_admin: # if admin redirect to admin page
                return redirect('/admin')
            else:
                return redirect('/') # redirect to homepage
        else:
            pass    
    
    return render_template('login.html')

# adding books to the database
@app.route('/add_book', methods =['GET','POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']

        # Create new book and add to library
        new_book = BookModel(title=title,author=author,isbn=isbn)
        db.session.add(new_book)
        db.session.commit()
        redirect('/admin')

    return render_template('add_book.html')

# remove a book from the database
@app.route('/remove_book', methods=['GET','POST'])
def remove_book():
    if request.method =='POST':
        isbn = request.form['isbn']

        # remove book from database
        book = BookModel.query.get(isbn)
        db.session.delete(book)
        db.session.commit()
        redirect('/admin')
    
    return render_template('remove_book.html')

# remove a user from the database
@app.route('/remove_user', methods=['GET','POST'])
def remove_user():
    if request.method == 'POST':
        email = request.form[email]

        # remove user from the database
        user = User.query.get(email)
        db.session.delete(user)
        db.session.commit()
        redirect('/admin')
    
    return render_template('remove_user.html')

if __name__ == "__main__":
    app.run(debug=True)