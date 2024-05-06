from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db
import sqlite3



app = Flask(__name__)
CORS(app)

# Initialize the database
init_db()

@app.route('/adduser', methods=['POST'])
def adduser():
    data = request.get_json()
    name = data['name']
    id = data['id']

    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Insert the incoming JSON data into the database
    c.execute('INSERT INTO names (id, name) VALUES (?, ?)', (id, name))
    conn.commit()

    # Query for names with IDs greater than 5
    c.execute('SELECT name FROM names WHERE id > 5')
    results = c.fetchall()

    # Prepare the list of names for the JSON response
    names_list = [name[0] for name in results]

    conn.close()

    return jsonify({"names_with_ids_above_5": names_list})

if __name__ == '__main__':
    app.run(debug=True)
