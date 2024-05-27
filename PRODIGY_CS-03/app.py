from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        strength = check_password_strength(password)
        return render_template('index.html', password=password, strength=strength)
    return render_template('index.html')

def check_password_strength(password):
    strength = 0
    if len(password) < 8:
        return "Weak"
    if not any(char.isdigit() for char in password):
        return "Weak"
    if not any(char.isupper() for char in password):
        return "Weak"
    if not any(char.islower() for char in password):
        return "Weak"
    if not any(not char.isalnum() for char in password):
        return "Medium"
    strength = "Strong"
    return strength

if __name__ == '__main__':
    app.run(debug=True)