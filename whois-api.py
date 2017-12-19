from flask import Flask, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = '****'
app.config['MYSQL_DATABASE_PASSWORD'] = '****'
app.config['MYSQL_DATABASE_DB'] = 'WHOIS'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/')
def get():
    cur = mysql.connect().cursor()
    cur.execute("""SELECT * FROM WHOIS_INFO """)
    r = [
        dict((cur.description[i][0], value) for i, value in enumerate(row))
        for row in cur.fetchall()
    ]
    return jsonify({'myCollection': r})


if __name__ == '__main__':
    app.run()
