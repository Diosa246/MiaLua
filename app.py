from flask import Flask,render_template, request,g,redirect,url_for 
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'books.db'  # This is the name of your SQLite database file

#initialzie db

def init_db():
    with sqlite3.connect(app.config['DATABASE']) as db:
        cursor = db.cursor ()
        cursor.execute('DROP TABLE IF EXISTS books')
        cursor.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                rating INTEGER NOT NULL
            )
        ''')
        db.commit()

#get database connection 
def get_db():
    if 'db' not in g: 
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES

        )
        g.db.row_factory = sqlite3.Row #allows access to columns by name 

    return g.db
    
#close db connection 
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)  # Get the database connection from 'g'

    if db is not None:
        db.close()  # Close the connection if it exists

#route & view function
@app.route('/')
def home():
    return render_template ('index.html')

#route to add books
@app.route('/add',methods=['POST'])
def add_book():
    title= request.form.get('title')
    author= request.form.get('author')
    genre= request.form.get('genre')
    rating= request.form.get('rating',0) #no response defaults to 0

    with get_db() as db: 
        cursor = db.cursor()
        cursor.execute('INSERT INTO books (title, author,genre, rating) VALUES (?, ?, ?,?)',
                    (title,author,genre,rating))
        db.commit()
    return redirect(url_for('home'))

@app.route('/books')
def view_books():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
    return render_template('books.html',books=books)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


