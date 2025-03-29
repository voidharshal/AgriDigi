from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "secret123"

users = []
crops = []

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        users.append({'username': username, 'password': password, 'role': role})
        print(users)

        return redirect(url_for('home'))
    
    return render_template('register.html')


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    for user in users:
        if user["username"] == username and user["password"] == password:
            session['username'] = username
            session['role'] = user['role']

            if user['role'] == 'farmer':
                return redirect(url_for('farmer_dashboard'))
            elif user['role'] == 'customer':
                return redirect(url_for('customer_dashboard'))
            elif user['role'] == 'supplier':
                return redirect(url_for('supplier_dashboard'))
            
    return "Invalid credentials. Please try again."

#farmer features
@app.route('/farmer_dashboard')
def farmer_dashboard():
    if 'username' in session and session['role'] == 'farmer':
        return render_template('farmer_dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/add_crop', methods=['POST'])
def add_crop():
    if 'username' in session and session['role'] == 'farmer':
        crop_name = request.form['crop_name']
        quantity = request.form['quantity']
        price = request.form['price']
        farmer = session['username']

        crops.append({'name': crop_name, 'quantity': quantity, 'price': price, 'farmer': farmer})
        return jsonify({'message': 'Crop added successfully!'})
    return jsonify({'message': 'Unauthorized access!'}), 403


@app.route('/view_crops')
def view_crops():
    if 'username' in session and session['role'] == 'farmer':
        farmer_crops = [crop for crop in crops if crop['farmer'] == session['username']]
        return jsonify(farmer_crops)
    return jsonify([])


@app.route('/customer_dashboard')
def customer_dashboard():
    if 'username' in session and session['role'] == 'customer':
        return render_template('customer_dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/supplier_dashboard')
def supplier_dashboard():
    if 'username' in session and session['role'] == 'supplier':
        return render_template('supplier_dashboard.html', username=session['username'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)