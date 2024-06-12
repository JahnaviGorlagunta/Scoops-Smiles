from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def setup_database():
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS seasonal_flavors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flavor TEXT NOT NULL,
                    description TEXT,
                    ingredients TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ingredient TEXT NOT NULL,
                    quantity INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flavor_suggestion TEXT NOT NULL,
                    customer_name TEXT,
                    allergy_concern TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS allergens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    allergen TEXT NOT NULL)''')

    # Prepopulate with some sample data
    c.executemany('INSERT INTO seasonal_flavors (flavor, description, ingredients) VALUES (?, ?, ?)',
                  [('Vanilla Bliss', 'Creamy vanilla ice cream', 'milk, sugar, vanilla'),
                   ('Chocolate Delight', 'Rich chocolate ice cream', 'milk, sugar, cocoa')])
    
    c.executemany('INSERT INTO inventory (ingredient, quantity) VALUES (?, ?)',
                  [('milk', 100), ('sugar', 50), ('vanilla', 20), ('cocoa', 30)])
    
    c.executemany('INSERT INTO allergens (allergen) VALUES (?)',
                  [('milk',), ('nuts',), ('gluten',)])

    conn.commit()
    conn.close()

setup_database()

@app.route('/')
def mainpage():
    return render_template('mainpage.html')

@app.route('/flavors')
def flavors():
    return render_template('index.html')

@app.route('/search_flavors', methods=['GET'])
def search_flavors():
    search_term = request.args.get('search_term', '')
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT id, flavor, description FROM seasonal_flavors WHERE flavor LIKE ? LIMIT 1', ('%' + search_term + '%',))
    result = c.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flavor_id = request.json.get('flavor_id')
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT flavor FROM seasonal_flavors WHERE id = ?', (flavor_id,))
    flavor = c.fetchone()
    if flavor:
        return jsonify({'message': f'Added {flavor[0]} to cart.'})
    else:
        return jsonify({'message': 'Flavor not found.'}), 404

@app.route('/add_allergen', methods=['POST'])
def add_allergen():
    allergen = request.json.get('allergen')
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT allergen FROM allergens WHERE allergen = ?', (allergen,))
    if c.fetchone():
        return jsonify({'message': 'Allergen already exists.'}), 400
    else:
        c.execute('INSERT INTO allergens (allergen) VALUES (?)', (allergen,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Allergen added.'})

if __name__ == '__main__':
    app.run(debug=True)
