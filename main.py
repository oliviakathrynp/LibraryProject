from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# ------ ORIGINAL WAY ------ #
# # creating connection to database
# db = sqlite3.connect("books-collection.db")
# # setup cursor to control/modify the database
# cursor =db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY , title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(3, 'Harry Potter and Deathly', 'J.K.Rowling', '9.3')")
# db.commit()
# -------- ORIGINAL WAY --------#

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#creating a new table
class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title

db.create_all()

#-----NEW WAY ------- #


@app.route('/')
def home():
    try:
        books = Book.query.order_by(Book.title).all()
    except Exception as e:
        print("Error: " + e)
    return render_template('index.html', book_list=books)

#crud operations

#CREATE

@app.route("/add", methods=['GET','POST'])
def add():
    if request.form:
        form_data = dict(request.form)
        book = Book(title=form_data['bookname'], author=form_data['author'], rating=form_data['rating'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

#READ
def read(_title):
    book = Book.query.filter_by(title=_title).first()
    return book

#UPDATE
@app.route("/update/<string:_title>")
def update_by_title(_title):
    return 'Update the following book: %s' %_title
    # update_book = Book.query.filter_by(title=_title).first()
    # update_book.title = new_title
    # db.session.commit() #not add because we are only updating new creating a new row


def update_by_key(key, new_title):
    update_book = Book.query.filter_by(id=key)
    update_book.title = new_title
    db.session.commit()

#DELETE
def delete_by_key(key):
    delete_book = Book.query.filter_by(id=key)
    db.session.delete(delete_book)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)

