from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from functions import Book, Member, Library
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Setup app to use SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

# Setup a simple table for the database
class BookModel(db.Model):
    title = db.Column(db.String(100),primary_key=True)
    author = db.Column(db.String(100))
    isbn = db.Column(db.Integer())

    def __repr__(self):
        return f"Book {self.title}"

class User(db.Model):
    email = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(100))

# Create tables in Database
with app.app_context():
    db.create_all()


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/create_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        member = User.query.get(email)
        if member == None:
            hashed_password = generate_password_hash(password)
            new_member = User(email=email,password=hashed_password)
            db.session.add(new_member)
            db.session.commit()
        redirect('/')
    
    return render_template('create_user.html')
    

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

    return render_template('add_book.html')

if __name__ == "__main__":
    app.run(debug=True)