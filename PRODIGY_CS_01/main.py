from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        shift = int(request.form['shift'])
        action = request.form['action']

        if action == 'encrypt':
            result = caesar_cipher_encrypt(message, shift)
        elif action == 'decrypt':
            result = caesar_cipher_decrypt(message, shift)

        return render_template('index.html', message=message, shift=shift, result=result, action=action)
    return render_template('index.html')

def caesar_cipher_encrypt(message, shift):
    result = ''
    for char in message:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_cipher_decrypt(message, shift):
    result = ''
    for char in message:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

if __name__ == '__main__':
    app.run(debug=True)