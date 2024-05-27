from flask import Flask, request, render_template, send_file
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        encryption_method = request.form['encryption_method']
        action = request.form['action']

        img = Image.open(image)
        img_array = np.array(img)

        if action == 'encrypt':
            if encryption_method == 'swap_pixels':
                encrypted_img_array = swap_pixels(img_array)
            elif encryption_method == 'add_value':
                encrypted_img_array = add_value(img_array, 10)
            else:
                encrypted_img_array = multiply_value(img_array, 2)
        else:
            if encryption_method == 'swap_pixels':
                encrypted_img_array = swap_pixels(img_array)
            elif encryption_method == 'add_value':
                encrypted_img_array = subtract_value(img_array, 10)
            else:
                encrypted_img_array = divide_value(img_array, 2)

        encrypted_img = Image.fromarray(encrypted_img_array)
        img_byte_arr = io.BytesIO()
        encrypted_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png')

    return render_template('index.html')

def swap_pixels(img_array):
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            temp = img_array[i, j, 0]
            img_array[i, j, 0] = img_array[i, j, 2]
            img_array[i, j, 2] = temp
    return img_array

def add_value(img_array, value):
    return img_array + value

def subtract_value(img_array, value):
    return img_array - value

def multiply_value(img_array, value):
    return img_array * value

def divide_value(img_array, value):
    return img_array // value

if __name__ == '__main__':
    app.run(debug=True)