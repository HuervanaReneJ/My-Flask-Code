from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "Huervana_1"

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'crud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students = data)

@app.route('/create', methods=['POST'])
def create():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        cur.execute("INSERT INTO students (name, email, phone, password) VALUES (%s, %s, %s, %s)", (name, email, phone, password) )
        conn.commit()
        flash('You Are Successfuly Added!')
        return redirect(url_for('index'))
    
@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', students = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_students(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""UPDATE students SET name = %s, email = %s, phone = %s, password = %s WHERE id = %s """, (name, email, phone, password, id))
        conn.commit()
        flash('Successfuly Updated!')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_students(id):
     conn = mysql.connect()
     cur = conn.cursor(pymysql.cursors.DictCursor)

     cur .execute('DELETE FROM students WHERE id = {0}' .format(id))
     conn.commit()
     flash('Successfuly Deleted!')
     return redirect(url_for('index'))
     


if __name__ == "__main__":
    app.run(port=3000, debug=True)