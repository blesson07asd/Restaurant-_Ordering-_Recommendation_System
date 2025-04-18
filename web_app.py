from flask import Flask, request, jsonify, send_from_directory
import csv
import os
import pandas as pd

# ✅ Importing the AI logic from your friend's file
from v1 import recommend

app = Flask(__name__)

# ---------- Serve Static Files ----------

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory('', 'style.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory('', 'script.js')

# ---------- CSV Helper Functions ----------

CSV_FILE = 'info.csv'

def read_users():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r') as file:
        return list(csv.DictReader(file))

def write_user(username, password):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password})

# ---------- Login API ----------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for user in read_users():
        if user['userid'] == username and user['password'] == password:
            return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'})

# ---------- Signup API ----------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Load existing users to check for duplicates
    with open('info.csv', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['userid'] == username:
                return jsonify({'success': False, 'message': 'Username already exists'})

    # Prepare a new row with 0 for all items
    new_user = {field: '0' for field in fieldnames}
    new_user['userid'] = username
    new_user['password'] = password

    # Append the new user
    with open('info.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(new_user)

    return jsonify({'success': True, 'message': 'Signup successful'})

# ---------- Recommendation API ----------

@app.route('/recommend', methods=['POST'])
def recommend_route():
    import pandas as pd
    from v1 import restrec

    data = request.get_json()
    username = data.get('username')

    df = pd.read_csv('info.csv')

    # Check if user exists
    if username not in df['userid'].values:
        return jsonify([])

    # Get user's purchase history (excluding userid and password)
    user_row = df[df['userid'] == username].iloc[0]
    food_data = user_row.drop(labels=['userid', 'password']).astype(int)

    # Check if the user has ever ordered anything (all 0s = new)
    if food_data.sum() == 0:
        return jsonify([])  # 👈 No recommendations for new user

    # If user has data, get actual recommendations
    obj = restrec()
    obj.username = username
    obj.df = df  # reusing the same dataframe

    recommendations = obj.recommend_items()
    return jsonify(recommendations)

# ---------- Menu Item Retrieval ----------

@app.route('/get_menu', methods=['GET'])
def get_menu():
    from v1 import restrec
    obj = restrec()  # this loads the items dictionary
    menu_list = []

    for code, item in obj.items.items():
        name = item[0]
        price = item[1]
        menu_list.append({'name': name, 'price': price})

    return jsonify(menu_list)

# ---------- Post Checkout Updates ----------

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    username = data['username']
    order = data['order']  # List of {name, quantity}

    updated = False
    rows = []
    with open('info.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['userid'] == username:
                for item in order:
                    item_name = item['name'].lower()
                    if item_name in row:
                        current_qty = int(row[item_name])
                        row[item_name] = str(current_qty + item['quantity'])
                updated = True
            rows.append(row)

    if not updated:
        return jsonify({'success': False, 'message': 'User not found.'})

    with open('info.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return jsonify({'success': True, 'message': 'Order updated successfully.'})

# ---------- Run Server ----------

if __name__ == '__main__':
    app.run(debug=True)

# from v1 import recommend

# @app.route('/recommend', methods=['POST'])
# def get_recommendation():
#     data = request.get_json()
#     username = data['username']
#     items = recommend(username)
#     return jsonify({'recommended': items})