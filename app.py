from flask import Flask, render_template, request, redirect, url_for, jsonify
import pyotp
import base64

app = Flask(__name__)

# Hardcoded admin user and password (for simplicity)
admin_username = "admin"
admin_password = "adminpassword"
otp_secret = base64.b32encode(b"admin123456789").decode('utf-8')  # Static OTP key for "admin"

# Simulating a simple user database
users = {"admin": {"password": admin_password, "email": "admin@gmail.com"}}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp = request.form['otp']

        if username in users and users[username]['password'] == password:
            # Check OTP using pyotp (TOTP)
            totp = pyotp.TOTP(otp_secret)
            if totp.verify(otp):
                return "Logged in successfully as " + username
            else:
                return "Invalid OTP", 400
        else:
            return "Invalid credentials", 400
    return render_template('login.html')

@app.route('/reset-pass', methods=['POST'])
def reset_password():
    username = request.json.get("username")
    email = request.json.get("email")
    # Simulate SMTP injection vulnerability
    # Allow attackers to inject another email
    if "admin" in email:  # Check for the injection payload
        users["admin"]["password"] = "newadminpassword"  # Reset admin password
        return jsonify({"message": "Password reset successful for admin!"}), 200
    return jsonify({"message": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
